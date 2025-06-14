document.addEventListener('DOMContentLoaded', function() {
    const headContent = `
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@100..900&display=swap" rel="stylesheet">
    `;
    document.head.insertAdjacentHTML('beforeend', headContent);

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
                            回到顶部
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
});