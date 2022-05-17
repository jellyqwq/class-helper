// 点击登录
$(document).ready(function() {
    $("#login").click(function(e){
        // e.preventDefault();
        // post
        $.post('/users/login',
            {
                'email': $("#email").val(),
                'pwd': $("#pwd").val()
            },
            function(data) {
                console.log(data)
                if (data.hasOwnProperty('error')) {
                    alert(data['error'])
                    // console.log(data['error']);
                }
                else
                {
                    $(location).attr('href', '/');
                    // console.log(data);
                } 
            }
        )
    })
});

// 回车登录
$(document).keyup(function(event){
    if (event.keyCode == 13) {
        $.post('/users/login',
            {
                'email': $("#email").val(),
                'pwd': $("#pwd").val()
            },
            function(data) {
                console.log(data)
                if (data.hasOwnProperty('error')) {
                    alert(data['error'])
                    // console.log(data['error']);
                }
                else
                {
                    $(location).attr('href', '/');
                    // console.log(data);
                } 
            }
        )
    }
});

// 注册跳转
$(document).ready(function() {
    $("#signup").click(function() {
        $(location).attr('href', '/register');
    })
})

// 忘记密码
$(document).ready(function() {
    $("#forget").click(function() {
        $(location).attr('href', '/forget')
    })
})