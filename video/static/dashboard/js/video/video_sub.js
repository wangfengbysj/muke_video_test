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
    }else if (success != null) {
        toastr.success(success, '消息')
    }

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
            }
        }
    }).on('success.form.bv', function (e) {
        console.log('success.form.bv');
        e.preventDefault();
        e.target.submit()
    })

    $('#videoSubResetBtn').click(function () {
        $('#videoSubForm').bootstrapValidator('resetForm', true);
    })

    $('#videoStarForm').bootstrapValidator({
        fields: {
            actorName:{
                validators: {
                    notEmpty: {
                        message: '演员不能为空'
                    }
                }
            },
            identity:{
                validators:{
                    notEmpty:{
                        message:'角色不能为空'
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