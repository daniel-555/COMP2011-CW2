$(document).ready(function () {
    $(".like-button").on("click", function () {
        var post_id = $(this).attr("id");
        console.log(`${post_id} button pressed`);
        $.ajax({
            type: "POST",
            url: "/like-post",
            data: JSON.stringify({ post_id: post_id }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: (response) => {
                console.log(response.message);
                $(this).text(`Like Post (${response.like_count})`);

                try {
                    if (response.status != 'liked already') {
                        var likes_received = Number($("#likes-received").text());
                        $("#likes-received").text(likes_received+1);
                    }
                } catch {}
            },
            error: (err) => console.log(err)
        });
    });
});