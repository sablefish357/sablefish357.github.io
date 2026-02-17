window.addEventListener('scroll', function() {
    const header = document.getElementById('header');
    const target1 = document.getElementById('target1').getBoundingClientRect().top;
    const target2 = document.getElementById('target2').getBoundingClientRect().top;
    const target3 = document.getElementById('target3').getBoundingClientRect().top;
    const target4 = document.getElementById('target4').getBoundingClientRect().top;
    const target5 = document.getElementById('target5').getBoundingClientRect().top;
    const target6 = document.getElementById('target6').getBoundingClientRect().top;
    const target7 = document.getElementById('target7').getBoundingClientRect().top;



    const bottom = document.getElementById('bottom').getBoundingClientRect().top;

    if ((target1 <= 40 && target2 >= 40) ||
        (target3 <= 40 && target4 >= 40) ||
        (target5 <= 40 && target6 >= 40) ||
        (target7 <= 40 && bottom >= 40 )
    ) {
        header.style.color = 'white'
    } else{
        header.style.color = 'black';
    }

});