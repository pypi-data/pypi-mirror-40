function sidebarplugin(trigger, sidebar, closetrigger) {
    if (sidebar) {
        var body = document.querySelector('body');
        var backdrop = document.querySelector('#backdrop');
        body.insertAdjacentHTML('beforeend', '<div class="dummyclass"></div>');
        closetrigger = closetrigger || document.querySelector('.dummyclass');
        console.log(sidebar);
        console.log(closetrigger);
        console.log(trigger);

        trigger.addEventListener('click', function() {
            sidebar.style.display = 'block';
            body.classList.add('sidebaropen');
            sidebar.classList.add('triggered');
        })


        backdrop.addEventListener('click', function() {
            sidebar.classList.remove('triggered');
            body.classList.remove('sidebaropen');
        })


        closetrigger.addEventListener('click', function() {
            sidebar.classList.remove('triggered');
            body.classList.remove('sidebaropen');

        })

    }
}
