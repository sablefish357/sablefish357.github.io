const headHTML = `
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@100..900&display=swap" rel="stylesheet">
`;
document.head.insertAdjacentHTML('beforeend', headHTML);

const filename = window.location.pathname.split('/').pop() || 'index.html';
const Link = filename.replace('.html','-zh.html');

const headerHTML = `
    <header id="header"> 
        <a href="/">
            <div class="SableFiSh">
                SableFiSh
            </div>
        </a>
        <a href="/">
            <div class="Studio">
                STUDIO
            </div>
        </a>
    </header>

    <nav id="top">
        <div class="leftbar">
            <a href="https://www.youtube.com/@SableFiSh">
                <div>VIDEOS</div>
            </a>
    
            <a href="/stages.html">
                <div>STAGES</div>
            </a>

            <a href="/blog.html">
                <div>BLOG</div>
            </a>

        </div>

        <div class="rightbar">

            <a href="/">
                <div>HOME</div>
            </a>

            <a href="#bottom">
                <div>CONTACT</div>
            </a>

            <a href="${Link}">
                <div>CHN</div>
            </a>
            
        </div>
    </nav>
`;
document.body.insertAdjacentHTML('afterbegin', headerHTML);

const footerHTML = `
    <footer id="bottom">
        <div class="footer-left">
            <div class="footer-container">
                <a href="https://www.youtube.com/@SableFiSh">
                    <div>
                        Youtube
                    </div>
                </a>
                <a href="https://space.bilibili.com/49323671">
                    <div>
                        Bilibili
                    </div>
                </a>
                <a href="https://www.artstation.com/sablefish">
                    <div>
                        ArtStation
                    </div>
                </a>
                <a href="mailto:sablefish357@gmail.com">
                    <div>
                        sablefish357@gmail.com
                    </div>
                </a>
                <a href="#top">
                    <div>
                        Top
                    </div>
                </a>
            </div>
            
            <div class="copyright">
                <div>
                    © 2024 SableFiSh. All Rights Reserved.
                </div>
            </div>
        </div>

        <div class="foot-logo-container">
            <a href="#top">
                <div class="SableFiSh">
                    SableFiSh
                </div>
            </a>
            <a href="#top">
                <div class="Studio">
                    STUDIO
                </div>
            </a>
        </div>

    </footer>
`;
document.body.insertAdjacentHTML('beforeend', footerHTML);


