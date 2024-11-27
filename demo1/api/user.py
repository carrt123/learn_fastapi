from fastapi import APIRouter, Depends, HTTPException
from demo1.dependencies import get_db_session
from demo1.db.database import AsyncSession
from demo1.services.user import UserServeries
from demo1.services.short import ShortServeries
from starlette.status import HTTP_401_UNAUTHORIZED
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta, datetime
from demo1.utils.hash_helper import HashHelper
from demo1.utils.auth_helper import AuthToeknHelper
from demo1.utils.random_helper import generate_short_url
from demo1.schemas import SingleShortUrlCreate
from fastapi import File, UploadFile

router_user = APIRouter(prefix="/api/v1", tags=["用户创建短链管理"])
# 注意需要请求的是完整的路径
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/oauth2/authorize")


@router_user.post("/oauth2/authorize", summary="请求授权URL地址")
async def login(user_data: OAuth2PasswordRequestForm = Depends(), db_session: AsyncSession = Depends(get_db_session)):
    if not user_data:
        raise HTTPException(status_code=400, detail="请输入用户账号及密码等信息")
    # 查询用户是否存在
    userinfo = await UserServeries.get_user_by_name(db_session, user_data.username)
    if not userinfo:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="不存在此用户信息",
            headers={"WWW-Authenticate": "Basic"}
        )

    # 验证用户密码和哈希密码值是否保持一直
    if not HashHelper.verify_password(user_data.password, userinfo.password):
        raise HTTPException(
            status_code=400,
            detail="用户密码不对"
        )

    # 签发JWT有效负载信息
    # iss: 签发者 issuer
    # sub: 主题 subject
    # admin: 是否是管理员
    # exp: 过期时间 expiration
    data = {
        'iss ': userinfo.username,
        'sub': 'god',
        'username': userinfo.username,
        'admin': True,
        'exp': datetime.utcnow() + timedelta(minutes=15)
    }
    # 生成Token
    token = AuthToeknHelper.token_encode(data=data)
    # access_token: 授权Token
    # token_type: 授权类型
    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router_user.post("/create/single/short", summary="创建单一短链请求")
async def create_single(create_info: SingleShortUrlCreate, token: str = Depends(oauth2_scheme),
                        db_session: AsyncSession = Depends(get_db_session)):
    try:
        payload = AuthToeknHelper.token_decode(token=token)
        # 获取用户名
        username = payload.get('username')
        # 生成短链信息
        create_info.short_tag = generate_short_url()
        create_info.short_url = f"{create_info.short_url}{create_info.short_tag}"
        create_info.created_by = username
        create_info.msg_context = f"{create_info.msg_context},了解详情请点击 {create_info.short_url} ！"

        # 启动数据库事务
        async with db_session.begin():
            result = await ShortServeries.create_short_url(db_session, **create_info.dict())

        # 如果成功，返回结果
        return {
            "code": 200,
            "msg": "创建短链成功",
            "data": {
                "short_url": result.short_url
            }
        }
    except Exception as e:
        # 如果出现异常，进行回滚
        await db_session.rollback()
        return {
            "code": 500,
            "msg": f"创建短链失败: {str(e)}"
        }


@router_user.post("/create/batch/short", summary="通过上传文件方式,批量创建短链")
async def create_batch(*, file: UploadFile = File(...),
                       token: str = Depends(oauth2_scheme),
                       db_session: AsyncSession = Depends(get_db_session)):

    try:
        # 解码并验证JWT
        payload = AuthToeknHelper.token_decode(token=token)
        username = payload.get('username')
        # 读取上传的文件内容
        contents = await file.read()
        batch_msg = contents.decode(encoding='utf-8').split("\n")

        # 构造短链的辅助函数

        def make_short_url(item):
            split_item = item.split("#")
            short_tag = generate_short_url()
            short_url = f"http://127.1.1.1:5000/{short_tag}"
            return SingleShortUrlCreate(
                long_url=f"{split_item[2]}{split_item[0]}",
                short_tag=short_tag,
                short_url=short_url,
                created_by=username,
                msg_context=f"{split_item[1].replace('chanename', split_item[0]).replace('url', 'short_url')}"
            )
        # 开启数据库事务
        async with db_session.begin():
            short_urls = [make_short_url(item) for item in batch_msg]
            await ShortServeries.create_batch_short_url(db_session, short_urls)
        # 返回成功响应
        return {
            "code": 200,
            "msg": "批量创建短链成功",
            "data": None
        }

    except Exception as e:
        # 如果发生异常，进行回滚
        await db_session.rollback()
        return {
            "code": 500,
            "msg": f"批量创建短链失败: {str(e)}"
        }
