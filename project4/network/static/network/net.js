document.addEventListener('DOMContentLoaded', function() {

    try{
      const elements = document.querySelectorAll('.likes_container');

      elements.forEach(element => {
        element.addEventListener('click', (e) => LikeOrUnlike_user(element)
        );
      });
    }catch(e){}

    try{
      document.querySelector('.follows_container').addEventListener('click', () => followOrUnfollow_user());
    }catch(e){}

    try{
      const edit_elements = document.querySelectorAll('.edit_post');

      edit_elements.forEach(element => {
        element.addEventListener('click', (e) => Edit_post(element)
        );
      });
    }catch(e){}
  });

function LikeOrUnlike_user(element) {

  parentDiv = element.parentNode
  post_id = parentDiv.querySelector('.post_id').textContent;
  likes = element.querySelector('#likes_counter').textContent;
  currentUrl = window.location.href
  fetchURL = ''

  if (currentUrl.includes("/user")){
    // Handling likes on user profile page
    fetchURL = '/post/like/'+post_id

  } else{
    // Handling likes on index page
    fetchURL = 'post/like/'+post_id

  }

  fetch(fetchURL, {
    method: 'PUT'
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Something went wrong');
    } else {
      if (element.querySelector('.heart_icon').alt === "like"){
        element.querySelector('.heart_icon').alt = "unlike"
        element.querySelector('.heart_icon').src = "\/static\/network/unlike.svg"
        element.title = "Unlike"

        likes = parseInt(likes) + 1
        element.querySelector('#likes_counter').textContent = likes

      } else if (element.querySelector('.heart_icon').alt === "unlike"){
        element.querySelector('.heart_icon').alt = "like"
        element.querySelector('.heart_icon').src = "\/static\/network/like.svg"
        element.title = "Like"

        likes = parseInt(likes) - 1
        element.querySelector('#likes_counter').textContent = likes
      }
    }
  })
}

function followOrUnfollow_user() {

  user = document.querySelector('#username').textContent;
  followers = document.querySelector('#followers_counter').textContent;

  fetch(user+'/follow', {
    method: 'PUT',
    credentials: 'include'
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Something went wrong');
    } else {
      if (document.querySelector('.follow_icon').alt === "follow"){
        document.querySelector('.follow_icon').alt = "unfollow"
        document.querySelector('.follow_icon').src = "\/static\/network/unfollow.svg"
        document.querySelector('.follow_text').textContent = "Unfollow"
        document.querySelector('.follow_text').style = "color: red"
    
        followers = parseInt(followers) + 1
        document.querySelector('#followers_counter').textContent = followers
    
      } else if (document.querySelector('.follow_icon').alt === "unfollow"){
        document.querySelector('.follow_icon').alt = "follow"
        document.querySelector('.follow_icon').src = "\/static\/network/follow.svg"
        document.querySelector('.follow_text').textContent = "Follow"
        document.querySelector('.follow_text').style = "color: green"
    
        followers = parseInt(followers) - 1
        document.querySelector('#followers_counter').textContent = followers

      }
    }
  })
}

function Edit_post(element) {

  showPostDiv = element.parentNode
  mainPostContainer = showPostDiv.parentNode
  editPostDiv = mainPostContainer.querySelector('.Edit_post_container')

  post_title = showPostDiv.querySelector('.post_title').innerText
  post_content = showPostDiv.querySelector('.post_content').innerText
  post_id = showPostDiv.querySelector('.post_id').innerText

  showPostDiv.style.display = 'none'
  editPostDiv.style.display = 'block'
  
  post_title_form = editPostDiv.querySelector('#post-title')
  post_content_form = editPostDiv.querySelector('#post-textarea')
  post_title_form.value = post_title
  post_content_form.value = post_content

  save_button = editPostDiv.querySelector('.btn')
  save_button.addEventListener('click', (event) => {
    event.preventDefault()

    title_value = post_title_form.value
    content_value = post_content_form.value

    fetch('/edit/'+post_id, {
      method: 'PUT',
      body: JSON.stringify({
          title: title_value,
          content: content_value
      })
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Something went wrong');
      } else {
        editPostDiv.style.display = 'none' 
        showPostDiv.querySelector('#post_edit_date').style.display = "block"
        showPostDiv.style.display = 'block'
        showPostDiv.querySelector('.post_title').innerText = title_value
        showPostDiv.querySelector('.post_content').innerText = content_value
        const d = new Date()
        showPostDiv.querySelector('#post_edit_date').innerText = 'Edited: '+d.toUTCString();

      }});
  })
}    