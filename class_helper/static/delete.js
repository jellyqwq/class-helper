// 返回设置页
$(document).ready(function() {
    $("#back").click(function() {
        $(location).attr('href', '/')
    })
})

// 校验邮箱并获取验证码
$(document).ready(function() {
    $("#verifycode").click(function() {
        if ($("#email").val() != '') {
           $.post('/sendvcode/resetpwd',
            {
                'email': $("#email").val()
            },
            function(data) {
                if (data.hasOwnProperty('error')) {
                    alert(data['error'])
                }
                else
                {
                    alert(data['result'])
                };
            }) 
        }
        else
        {
            alert('邮箱不能为空')
        }
    })
})

// 密码重置
$(document).ready(function() {
    $("#resetpwd").click(function() {
        // console.log($("#email").val())
        if ($("#email").val() == '') {
            alert('邮箱不能为空')
        }
        else
        {
            var pwd1 =  $("#pwd1").val()
            var pwd2 = $("#pwd2").val()
            // console.log(pwd1)
            // console.log(pwd2)
            if (pwd1 == '' || pwd2 == '') {
                alert('密码不能为空')
            }
            else
            {
                if (pwd1 == pwd2) {
                    console.log($("#inputverifycode").val())
                    if ($("#inputverifycode").val() == '') {
                        alert('验证码不能为空')
                    }
                    else
                    {
                        $.post('/user/resetpwd', {
                            'email': $("#email").val(),
                            'pwd': pwd1,
                            "sc": $("#inputverifycode").val()
                        },
                        function(data) {
                            if (data.hasOwnProperty('error')) {
                                alert(data['error'])
                            }
                            else
                            {
                                alert(data['success'])
                                $(location).attr('href', '/');
                            };
                        })
                    }
                }
                else
                {
                    alert('密码不一致')
                }
            }
        }
    })
})

// 删除账号
$(document).ready(function() {
    $('#DeleteAccount').click(function() {
        if ($("#email").val() == '') {
            alert('邮箱不能为空')
        }
        else
        {
            if ($('#inputverifycode').val() == '') {
                alert('验证码不能为空')
            }
            else
            {
                $.post('/user/delete', {
                    'email': $('#email').val(),
                    'sc': $('#inputverifycode').val()
                },
                function(data) {
                    if (data.hasOwnProperty('error')) {
                        alert(data['error'])
                    }
                    else
                    {
                        alert(data['success'])
                        $(location).attr('href', '/');
                    };
                })
            }
        }
    })
})