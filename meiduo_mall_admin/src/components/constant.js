let cons = {
	apis:'http://127.0.0.1:8000/meiduo_admin' // 远程地址
	//apis:'http://172.16.21.25:8001/meiduo_admin'
}

if (process.env.NODE_ENV === 'production') {
  cons = {
	apis:'http://47.98.181.79:6011/meiduo_admin' // 服务器的地址
}
}

export default cons
