// workaround for adding animated loading buttons in Django using vanilla javascript
window.addEventListener('load', (event) => {
    const form = document.querySelector("form[method=POST]")
    if(form){
        // if there is a form get the submit button and get it's classes
        const preClickBtn = document.querySelector('input[type=submit]')
        const classesForBtn = preClickBtn.className
        form.addEventListener('submit', (event) => {
            // on submit check if we want a small or full width button and replace the old button
            const isWindowSmall = window.innerWidth < 575
            const postClickBtnDiv = document.createElement('div')
            postClickBtnDiv.style.display = 'inline'
            // retain all classes and set width to 100% if window is small
            postClickBtnDiv.innerHTML = `
                <button 
                    class="${classesForBtn}" 
                    type="button" 
                    ${isWindowSmall && "style='width:100%;'"} 
                    disabled>
                    
                    <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                    Loading, please wait...
                </button>`
            preClickBtn.parentNode.replaceChild(postClickBtnDiv, preClickBtn)
        })
    }
})