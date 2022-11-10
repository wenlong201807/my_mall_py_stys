var vm = new Vue({
    el: '#app',
	// 修改Vue变量的读取语法，避免和django模板语法冲突
    delimiters: ['{{', '}}'],
    data: {
        host,
        error_username: false,
        error_password: false,
		error_username_message: '请输入5-20个字符的用户名',
		error_password_message: '请输入8-12位的密码',
        username: '',
        password: '',
        remembered: true
    },
    methods: {
        // 检查账号
        check_username: function(){
        	var re = /^[a-zA-Z0-9_-]{5,20}$/;
			if (re.test(this.username)) {
                this.error_username = false;
            } else {
                this.error_username = true;
            }
        },
		// 检查密码
        check_pwd: function(){
        	var re = /^[0-9A-Za-z]{8,20}$/;
			if (re.test(this.password)) {
                this.error_password = false;
            } else {
                this.error_password = true;
            }
        },
        // 表单提交
        on_submit: function(){
            this.check_username();
            this.check_pwd();

            if (this.error_username || this.error_password) {
                // 不满足登录条件：禁用表单
				window.event.returnValue = false
            }
        },
        getQueryString(url, paraName) {
          const arrObj = url.split("?");
          if (arrObj.length > 1) {
            const arrPara = arrObj[1].split("&");
            let arr;
            for (let i = 0; i < arrPara.length; i++) {
                arr = arrPara[i].split("=");
              // eslint-disable-next-line eqeqeq
              if (arr != null && arr[0] == paraName) {
                return arr[1];
              }
            }
            return "";
          } else {
            return "";
          }
        },
        // qq登录
        qq_login: function(){
            var next = get_query_string('next') || '/';
            var url = this.host + '/qq/login/?next=' + next;
            axios.get(url, {
                    responseType: 'json'
                })
                .then(response => {
                    // 'https://graph.qq.com/oauth2.0/authorize?' + urlencode(data_dict)

                    // https://graph.qq.com/oauth2.0/show?which=error&display=pc&error=100010&which=Login&display=pc&response_type=code&client_id=101518219&state=%2F&redirect_uri=http%25253A%25252F%25252Fwww.meiduo.site%25253A8000%25252Foauth_callback
                    // https://graph.qq.com/oauth2.0/show?which=error&display=pc&error=100010&which=Login&display=pc&response_type=code&client_id=101518219&state=%2F&redirect_uri=http://www.meiduo.site:8000/oauth_callback
// https://graph.qq.com/oauth2.0/show?which=error&display=pc&error=100010&which=Login&display=pc&response_type=code&client_id=101518219&state=%2F&redirect_uri=http://www.meiduo.site:8000/oauth_callback
// 1546683858 qaz3579
                    const qqUrl = `https://graph.qq.com/oauth2.0/show?which=Login&display=pc&redirect_uri=http://www.meiduo.site:8000/oauth_callback&response_type=code&client_id=101518219&state=%2F`

                    // location.href = response.data.login_url;  // 扫码成功后，自动跳转到 qq授权页面
                    location.href = qqUrl;  // 扫码成功后，自动跳转到 qq授权页面
                })
                .catch(error => {
                    console.log(error.response);
                })
        }
    }
});
