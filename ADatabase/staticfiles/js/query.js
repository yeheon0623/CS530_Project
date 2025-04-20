$("#btn_q1").click(function () {
    const UserID = $("#UserID").val();
    if (!UserID) return;

    $("#result_q1").html(`
      <iframe id="dash-frame" src="/dash/app/useranalytics/?user_id=${UserID}" width="100%" height="600" style="border:none;"></iframe>
    `);
});



$("#btn_q2").click(function(){  
    console.log('q2hhhh');
    var KeyWord =$("#KeyWord").val()
    $.ajax({
        type : "POST",
        url : "query2/",
        dataType : "html",
        data: {
            csrfmiddlewaretoken: '{{ csrf_token }}',
            KeyWord: KeyWord,
        },
        async : true,
        success : function(data) {
            $("#KeyWord").val(KeyWord); 
            $("#result_q2").html(data); 
        },
        error : function() {
            alert('Request error');
        }
    });
    });

$("#btn_q3").click(function(){  
    console.log('q3hhhh');
    var Style =$("#Style").val()
    $.ajax({
        type : "POST",
        url : "query3/",
        dataType : "html",
        data: {
            csrfmiddlewaretoken: '{{ csrf_token }}',
            Style: Style,
        },
        async : true,
        success : function(data) {
            $("#Style").val(Style); 
            $("#result_q3").html(data); 
        },
        error : function() {
            alert('Wrong request');
        }
    });
    });