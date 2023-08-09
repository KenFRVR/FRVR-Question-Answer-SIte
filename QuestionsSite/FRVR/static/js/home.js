'use strict';

// A '#' symbol indicates that it works, but it needs to be reformatted or clean

const $showAnswersBtns = document.querySelectorAll(".show-answers")
const $readMoreAnchors = document.querySelectorAll('.read-more')
const $commentForms = document.querySelectorAll('.comment-form')

$showAnswersBtns.forEach(btn => {
    btn.addEventListener("click", (e) => {

        // Get question ID from the parent element
        const questionId = e.target.parentElement.id
        const $answersSection = document.querySelector('#answers-' + questionId)
        toggleComments($answersSection)
    })
})

$commentForms.forEach(form => {
    form.addEventListener("submit", (e) => {

        // Prevent the page reload
        e.preventDefault()

        // # Get first comment so the new one can be added before it #
        const $firstComment = form.parentElement.nextElementSibling

        // # Get comment container to insert the new Comment in case there is no one #
        const $commentsContainer = form.parentElement.parentElement

        // Get form data
        const formData = new FormData(form)

        // Options to fetch
        const options = {
            method: 'POST',
            body: formData
        }

        // Fetch data
        fetchData('', options)
            .then(data => {
                const $newComment = `<div class="comment-container right">
                                        <p class="text right">
                                            <span class="comment-author">${capitalize(data.username)}: </span>
                                            ${data.text}
                                            <span class="comment-time">${getTime(data.time)}</span>
                                        </p>
                                    </div>`

                if ($firstComment !== null) {
                    $firstComment.insertAdjacentHTML('beforebegin', $newComment)
                } else {
                    $commentsContainer.innerHTML += $newComment
                }

                const $commentCounter = document.querySelector(`#${data.counter}`)
                $commentCounter.textContent = parseInt($commentCounter.textContent) + 1

                const $answerCounter = document.querySelector('#answers-counter')
                $answerCounter.textContent = parseInt($answerCounter.textContent) + 1
            }).catch(err => {
            console.log(err)
        })

    })
})


$readMoreAnchors.forEach(a => {
    a.addEventListener("click", (e) => {
        e.preventDefault()
        const target = e.target
        const $questionText = target.previousElementSibling
        toggleText(target, $questionText)
    })
})


function toggleComments(e) {
    e.classList.toggle('active')
}

function toggleText($link, $text) {

    if ($text.classList.contains('expanded')) {
        $text.textContent = $link.dataset.summary
        $text.classList.remove('expanded')
        $link.textContent = 'Read more'
    } else {
        $text.textContent = $link.dataset.fulltext
        $text.classList.add('expanded')
        $link.textContent = 'Read less'
    }
}

function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1)
}

function getTime(datetime) {
    return new Date(datetime).toLocaleTimeString()
}

function fetchData(url, options) {
    return new Promise((resolve, reject) => {
        fetch(url, options)
            .then(response => response.json())
            .then(data => {
                resolve(data)
            }).catch(error => {
            reject(error)
        })
    })
}