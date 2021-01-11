$(function () {

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

    // 附加信息对话框关闭后reest表单
    $('#videoAddtionDialog').on('hide.bs.modal', function () {
        $('#videoSubForm').bootstrapValidator('resetForm', true)
    })

    // 演员对话框关闭后reset表单
    $('#actorDialog').on('hide.bs.modal', function () {
        $('#videoStarForm').bootstrapValidator('resetForm', true)
        $('#identity').val('director')
    })

    // 弹出添加视频附加信息对话框
    $('#videoAdditionBtn').click(function () {
        $('#actorTitle').text("添加演员信息")
        $('#videoAddtionDialog').modal('show')
    })

    // 弹出添加演员对话框
    $('#videoStarBtn').click(function () {
        $('#actorTitle').text("添加附加信息")
        $('#actorDialog').modal('show')
    })

    // 视频附加信息表单验证
    $('#videoSubForm').bootstrapValidator({
        fields: {
            url: {
                validators: {
                    notEmpty: {
                        message: "添加地址不能为空"
                    },
                    uri: {
                        message: '地址验证错误'
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

    // 演员表单验证
    $('#videoStarForm').bootstrapValidator({
        fields: {
            actorName: {
                validators: {
                    notEmpty: {
                        message: '演员不能为空'
                    }
                }
            },
            identity: {
                validators: {
                    notEmpty: {
                        message: '角色不能为空'
                    }
                }
            }
        }
    }).on('success.form.bv', function (e) {
        console.log('success.form.bv');
        e.preventDefault();
        e.target.submit()
    })

    // 提交演员表单
    $('#actorOkBtn').click(function () {
        $('#videoStarForm').submit()
    })
})
