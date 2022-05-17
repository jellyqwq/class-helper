// 登出
$(document).ready(function() {
    $("#logout").click(function(){
        $.post('/users/logout',
            function(data) {
                // console.log(data)
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
})

// 提交
$(document).ready(function(){
    $("#submit").click(function(){
        // 判断每个复选框的状态
        if ($('#switch_pushplus').is(':checked')) {
            var switch_pushplus = true
        }
        else
        {
            var switch_pushplus = false
        }
        if ($('#switch_telegram').is(':checked')) {
            var switch_telegram = true
        }
        else
        {
            var switch_telegram = false
        }
        if ($('#switch_weather').is(':checked')) {
            var switch_weather = true
        }
        else
        {
            var switch_weather = false
        }
        if ($('#switch_pushplus_rightnow').is(':checked')) {
            var switch_pushplus_rightnow = true
        }
        else
        {
            var switch_pushplus_rightnow = false
        }
        if ($('#switch_telegram_rightnow').is(':checked')) {
            var switch_telegram_rightnow = true
        }
        else
        {
            var switch_telegram_rightnow = false
        }
        
        // 提交内容
        $.post('/submit',
            {
                'name': $("#user_name").val(),
                'openid': $("#openid").val(),
                'xh': $("#xh").val(),
                'pushplustoken': $("#pushplustoken").val(),
                'tgtoken': $("#tgtoken").val(),
                'tg_user_id' : $("#tg_user_id").val(),
                'switch_pushplus' : switch_pushplus,
                'switch_telegram': switch_telegram,
                'switch_weather': switch_weather,
                'switch_pushplus_rightnow': switch_pushplus_rightnow,
                'switch_telegram_rightnow': switch_telegram_rightnow
            },
            function (data) {
                if (data.hasOwnProperty('error')) {
                    alert(data.error)
                }
                else
                {
                    alert(data['result'])
                }
            }
        )
    })
});

// 回车提交
$(document).keyup(function(event){
    if (event.keyCode == 13) {
        $("#submit").click(function(){
            // 判断每个复选框的状态
            if ($('#switch_pushplus').is(':checked')) {
                var switch_pushplus = true
            }
            else
            {
                var switch_pushplus = false
            }
            if ($('#switch_telegram').is(':checked')) {
                var switch_telegram = true
            }
            else
            {
                var switch_telegram = false
            }
            if ($('#switch_weather').is(':checked')) {
                var switch_weather = true
            }
            else
            {
                var switch_weather = false
            }
            if ($('#switch_pushplus_rightnow').is(':checked')) {
                var switch_pushplus_rightnow = true
            }
            else
            {
                var switch_pushplus_rightnow = false
            }
            if ($('#switch_telegram_rightnow').is(':checked')) {
                var switch_telegram_rightnow = true
            }
            else
            {
                var switch_telegram_rightnow = false
            }
            
            // 提交内容
            $.post('/submit',
                {
                    'name': $("#user_name").val(),
                    'openid': $("#openid").val(),
                    'xh': $("#xh").val(),
                    'pushplustoken': $("#pushplustoken").val(),
                    'tgtoken': $("#tgtoken").val(),
                    'tg_user_id' : $("#tg_user_id").val(),
                    'switch_pushplus' : switch_pushplus,
                    'switch_telegram': switch_telegram,
                    'switch_weather': switch_weather,
                    'switch_pushplus_rightnow': switch_pushplus_rightnow,
                    'switch_telegram_rightnow': switch_telegram_rightnow
                },
                function (data) {
                    if (data.hasOwnProperty('error')) {
                        alert(data.error)
                    }
                    else
                    {
                        alert(data['result'])
                    }
                }
            )
        })
    }
});

// 跳转到删除页面
$(document).ready(function () {
    $('#delete').click(function () {
        $(location).attr('href', '/delete')
    })
})