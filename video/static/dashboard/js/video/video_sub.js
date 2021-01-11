$(function () {

    $.getUrlParam = function (name) {
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
        var r = window.location.search.substr(1).match(reg);
        if (r != null) return decodeURI(r[2]);
        return null;
    }

    var error = $.getUrlParam('error');
    var success = $.getUrlParam('success')
    if (error != null) {
        toastr.error(error, '警告')
    } else if (success != null) {
        toastr.success(success, '消息')
    }

    $('#videoAddtionDialog').on('hide.bs.modal', function () {
        $('#videoSubForm').bootstrapValidator('resetForm', true)
    })

    // 弹出视频附加信息对话框
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

    $('#videoActorResetBtn').click(function () {
        $('#videoStarForm').bootstrapValidator('resetForm', true);
        $('#identity').val('director')
    })


})