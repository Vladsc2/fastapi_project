

async def wrap_html(text: str) -> str:
    prefix = """
        <style>
            body {
                background: #121212;
                padding-top: 8%;
                margin: 0;
                font-size: 2.5vh;
            }
            pre {
                font-family: inherit;
                white-space: pre-wrap;
                color: #f0f0f0;

                margin-left: 5%;
                margin-right: 28%;
                word-wrap: break-word;
                overflow-wrap: break-word;
            }
            pre a {
                text-decoration: none;
                color: orange;
            }
            pre a:hover {
                color: darkorange;
            }
            .toolbar {
                position: fixed;
                top: 3%;
                right: 3%;
                width: 20%;
                background: #1e1e1e;
                border-radius: 12px;
                padding: 12px;
                display: flex;
                flex-direction: row;
                gap: 2vw;
                box-shadow: 0 2px 10px rgba(0,0,0,0.5);
                z-index: 1000;
            }
            .section {
                display: flex;
                flex-direction: column;
                gap: 8px;
            }
            .section-title {
                font-size: 12px;
                color: #aaa;
                text-align: center;
                margin-bottom: 4px;
                letter-spacing: 1px;
            }
            .toolbar a {
                text-decoration: none;
                background: #333;
                color: white;
                padding: 6px 12px;
                border-radius: 6px;
                text-align: center;
                font-size: 14px;
                transition: background 0.2s;
            }
            .toolbar a:hover {
                background: #555;
            }
        </style>

        <div class="toolbar">
            <div class="section">
                <div class="section-title">🗡️ ПЕРСОНАЖ</div>
                <a href="/inventory">🎒 Инвентарь</a>
                <a href="/character">🧑 Характеристики</a>
            </div>
            <div class="section">
                <div class="section-title">🎲 КОСТИ</div>
                <a href="/roll?dice=2&times=1">d2</a>
                <a href="/roll?dice=4&times=1">d4</a>
                <a href="/roll?dice=6&times=1">d6</a>
                <a href="/roll?dice=8&times=1">d8</a>
                <a href="/roll?dice=10&times=1">d10</a>
                <a href="/roll?dice=12&times=1">d12</a> 
                <a href="/roll?dice=20&times=1">d20</a>
                <a href="/roll?dice=percent&times=1">percent</a>
            </div>
        </div>

        <pre>
"""

    postfix = "\n</pre>"


    return prefix + text + postfix