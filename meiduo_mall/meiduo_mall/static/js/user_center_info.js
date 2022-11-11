var vm = new Vue({
    el: '#app',
    // 修改Vue变量的读取语法，避免和django模板语法冲突
    delimiters: ['{{', '}}'],
    data: {
        host: host,
        username: username, // 在html中类似全局变量传入此处，变成vue里头的初始化数据
        mobile: mobile,
        email: email,
        email_active: email_active,
        set_email: false,
        error_email: false,
        error_email_message: '',
        send_email_btn_disabled: false,
        send_email_tip: '重新发送验证邮件',
        histories: []
    },
    // ES6语法
    mounted() {
        // 额外处理用户数据
        // this.email_active = this.email_active;
        this.set_email = !this.email;

        // 请求浏览历史记录
        this.browse_histories();
    },
    methods: {
        // 检查email格式
        check_email(){
            var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;
            if (re.test(this.email)) {
                this.error_email = false;
            } else {
                this.error_email_message = '邮箱格式错误';
                this.error_email = true;
                return;
            }
        },
        // 取消保存
        cancel_email(){
            this.email = '';
            this.error_email = false;
        },
        // 保存email
        save_email(){
            // 检查email格式
            this.check_email();

            if (!this.error_email) {
                var url = this.host + '/emails/';
                axios.put(url, {
                    //  能够发这个请求，说明已经是登录状态，那么后端是有现成的用户其他信息的，只缺一个email字段信息
                        email: this.email
                    }, {
                        headers: {
                            'X-CSRFToken':getCookie('csrftoken')
                        },
                        responseType: 'json'
                    })
                    .then(response => {
                        if (response.data.code === '0') {
                            this.set_email = false;
                            this.send_email_btn_disabled = true;
                            this.send_email_tip = '已发送验证邮件';
                        } else if (response.data.code === '4101') {
                            // 后端会检测，如果不是登录态，需要先登录，再自动跳转到这个页面继续操作
                            location.href = '/login/?next=/info/';
                        } else { // 5000 5001
                            this.error_email_message = response.data.errmsg;
                            this.error_email = true;
                        }
                    })
                    .catch(error => {
                        console.log(error.response);
                    });
            }
        },
        // 请求浏览历史记录
        browse_histories(){
            var url = this.host + '/browse_histories/';
            axios.get(url, {
                    responseType: 'json'
                })
                .then(response => {
                    this.histories = response.data.skus;
                    for(let i=0; i<this.histories.length; i++){
                        this.histories[i].url = '/goods/' + this.histories[i].id + '.html';
                    }
                })
                .catch(error => {
                    console.log(error.response);
                })
        }
    }
});
