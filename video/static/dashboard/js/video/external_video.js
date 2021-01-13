$(document).ready(function () {

    // 获取页面请求查询参数
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

    // 弹出视频表单对话框
    $('#createBtn').click(function () {
        $('#videoTitle').text('添加视频信息')
        $('#video_type').val('movie')
        $('#from_to').val('youku')
        $('#nationality').val('china')
        $('#video_id').val('')
        $('#myModal').modal('show')
    })

    // 视频表单提交
    $('#videoSubmitBtn').click(function () {
        $('#videoForm').submit()

    });

    // 视频表单验证
    $('#videoForm').bootstrapValidator('validate')
        .on('success.form.bv', function (e) {
            console.log('success.form.bv');
            e.preventDefault();
            e.target.submit()
        });

    // 关闭对话框时reset表单
    $('#myModal').on('hide.bs.modal', function () {
        $('#videoForm').bootstrapValidator('resetForm', true)
        $('#videoForm')[0].reset()
    })

    // 编辑视频信息
    $('.videoBtn').click(function () {
        var video_id = $(this).attr('data-id')
        // alert($("#videoForm").serialize())
        $('#videoTitle').text('编辑视频信息')
        $.ajax({
            type:'GET',
            url:'/dashboard/video/external/update/'+video_id,
            dataType:'json',
            // data:$("#videoForm").serialize(), 更新表单，不需要提交表单数据
            success:function (data) {
                $('#video_id').val(data['pk'])
                $('#name').val(data.fields['name'])
                $('#image').val(data.fields['image'])
                $('#video_type').val(data.fields['video_type'])
                $('#from_to').val(data.fields['from_to'])
                $('#nationality').val(data.fields['nationality'])
                $('#info').val(data.fields['info'])
                $('#myModal').modal('show')
            }
        })
    })
});