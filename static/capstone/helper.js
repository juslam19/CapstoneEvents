function update_like_button(id) {
    var like_button = document.querySelector(`#like-${id}-button`);
    var like_count = document.querySelector(`#like-${id}-count`);

    fetch('/like_helper/'+ id)
        .then(response => response.json())
        .then(data => helper(data));

    function helper(data) {
        if (data['message'] == 'error') {
            like_button.style.color = 'black';
        } else if (data['message'] == 'success') {
            like_button.style.color = 'red';
        } else {
            // DO NOTHING
            // For error checking
        }
    }

}

function confirm(id) {
    var delete_button = document.querySelector(`#delete-${id}`);
    var delete_confirm_button = document.querySelector(`#delete-${id}-confirm`);
    var delete_confirm_message = document.querySelector(`#delete-${id}-confirm-message`);

    if (delete_confirm_button.style.display == 'none') {
        delete_confirm_button.style.display = 'block';
        delete_confirm_message.style.display = 'block';
        delete_button.innerHTML = "Don't Delete";
    } else {
        delete_confirm_button.style.display = 'none';
        delete_confirm_message.style.display = 'none';
        delete_button.innerHTML = "Delete";
    }
}

function like(id) {
    var like_button = document.querySelector(`#like-${id}-button`);
    var like_count = document.querySelector(`#like-${id}-count`);

    like_button.addEventListener('click', () => {

        async function like_unlike() {
            const response = await fetch('/like_helper/'+ id);
            const data = await response.json();
            console.log(data);

            function update_like_button(data) {
                if (data['message'] == 'error') {
                    const request_options = {
                        method: 'PUT',
                        body: JSON.stringify({
                            like: true
                        })
                      };
                    fetch('/like/' + id, request_options);

                    like_button.style.color = 'red';
                } else if (data['message'] == 'success') {
                    const request_options = {
                        method: 'PUT',
                        body: JSON.stringify({
                            like: false
                        })
                      };
                    fetch('/like/' + id, request_options);

                    like_button.style.color = 'black';
                } else {
                    // DO NOTHING
                    // For error checking
                }
                return false;
            }

            const first = await update_like_button(data);
            return false;
        }

        async function update_like_count() {
            const response = await fetch('/like/'+ id);
            const post = await response.json();
            console.log(post);

            like_count.innerHTML = post.likes;
            return false;
        }

        async function start() {
            const first = await like_unlike();
            const second = await update_like_count();
        }

        start();
    });

}