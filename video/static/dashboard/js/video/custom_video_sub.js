$(document).ready(function () {
    $('.list-group-item').removeClass('active')
    $('#selfVideoMenu').addClass('active')

    // 获取URL中的error和success参数
    $.getUrlParam = function (name) {
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
        var r = window.location.search.substr(1).match(reg);
        if (r != null) return decodeURI(r[2]);
        return null;
    }

    // 页面初始化显示错误或者成功消息
    var error = $.getUrlParam('error');
    var success = $.getUrlParam('success')
    if (error != null) {
        toastr.error(error, '警告')
    } else if (success != null) {
        toastr.success(success, '消息')
    }

    // 弹出添加视频附加信息对话框
    $('#videoAdditionBtn').click(function () {
        $('#videoAddtionTitle').text("添加附加信息")
        $('#videoAddtionDialog').modal('show')
    })

    // 视频附加信息表单验证
    $('#videoSubForm').bootstrapValidator({
        fields: {
            url: {
                validators: {
                    notEmpty: {
                        message: "上传视频不能为空"
                    },
                    file: {
                        extension: 'mp4,mpg',
                        type: 'video/mp4,video/mpeg',
                        message: '请选择视频文件'
                    }
                }
            },
            number: {
                validators: {
                    notEmpty: {
                        message: "集数不能为空"
                    },
                    digits: {
                        message: '只能添加正数'
                    }
                }
            }
        }
    }).on('success.form.bv', function (e) {
        console.log('success.form.bv');
        e.preventDefault();
        e.target.submit()
    })

    // 提交视频信息附加表单
    $('#videoAddtionOkBtn').click(function () {
        $('#videoSubForm').submit()
    })
})