// Query 1: Load user analytics dashboard
$("#btn_q1").click(function () {
    const UserID = $("#UserID").val();
    if (!UserID) return;

    $("#result_q1").html(`
      <iframe id="dash-frame" src="/dash/app/useranalytics/?user_id=${UserID}" width="100%" height="600" style="border:none;"></iframe>
    `);
});

// Pagination state for Query 2
let q2_page = 0;
let q2_mode = "basic";

function fetchQuery2Results() {
    const KeyWord = $("#KeyWord").val();
    $.ajax({
        type: "POST",
        url: "query2/",
        dataType: "html",
        data: {
            csrfmiddlewaretoken: '{{ csrf_token }}',
            KeyWord: KeyWord,
            mode: q2_mode,
            page: q2_page
        },
        async: true,
        success: function (data) {
            $("#result_q2").html(data);
        },
        error: function () {
            alert('Search failed');
        }
    });
}

// Query 2: Basic match
$("#btn_q2_basic").click(function () {
    q2_page = 0;
    q2_mode = "basic";
    fetchQuery2Results();
});

// Query 2: Full-text search
$("#btn_q2_fts").click(function () {
    q2_page = 0;
    q2_mode = "fts";
    fetchQuery2Results();
});

// Query 2: Next button (pagination)
$(document).on("click", ".btn-page", function () {
    q2_page = parseInt($(this).data("page"));
    fetchQuery2Results();
});

// Query 3: Style search
$("#btn_q3").click(function () {
    console.log('q3hhhh');
    var Style = $("#Style").val();
    $.ajax({
        type: "POST",
        url: "query3/",
        dataType: "html",
        data: {
            csrfmiddlewaretoken: '{{ csrf_token }}',
            Style: Style,
        },
        async: true,
        success: function (data) {
            $("#Style").val(Style);
            $("#result_q3").html(data);
        },
        error: function () {
            alert('Wrong request');
        }
    });
});
