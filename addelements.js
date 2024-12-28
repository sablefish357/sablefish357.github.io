document.addEventListener('DOMContentLoaded', function() {
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
});


