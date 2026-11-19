# Little Things — Jezneel's strawberry birthday adventure

A mobile-first, interactive birthday website with a procedural Three.js kitchen and a self-contained illustrated SVG alternative. The story is built around the wrong-number memory, then a strawberry cake and a personal birthday letter. The letter text is exactly as supplied.

## Run and share

Use Node 20.19+ or 22.12+. Extract the archive, then run:

```sh
npm install
npm run dev
```

Open the printed URL. To test on your phone on the same Wi-Fi network, use the Network URL printed by Vite, allowing access through the firewall if needed. To deploy:

```sh
npm run build
```

Upload `dist/` to a static host, or connect the project to Netlify using the supplied `netlify.toml`. Jezneel only needs the resulting HTTPS URL, not Node or an app installation. The message is visible to anyone with the URL; use access-controlled hosting if necessary.

You can also open `preview.html` without installing anything. It is a dependency-free illustrated version (not Three.js), built from the same game logic. It can itself be hosted as a static HTML file if there is no time to verify the 3D build.

## Experience checklist

1. Dark chat introduction: animated messages, wrong-number joke, tap to unlock audio.
2. Four frosting colors, which set the accent, cake frosting and confetti.
3. Flour, sugar, butter: drag into the bowl or tap. Egg: tap to crack; two shell halves separate and the yolk and white drop into the bowl. Continue only when all ingredients are in.
4. Draw circles over the bowl to mix, or use the accessible stir button. Animated whisk and batter. A separate animated tilt-and-pour sequence transfers the batter to the pan.
5. Oven: open the bottom-hinged door, slide the pan onto its rack (or use the button), close the door, watch a six-second countdown and the cake rise. Peek zooms in while it bakes. The oven light flickers, the timer dings, then open and remove the cake with a separate animation.
6. Swipe to spread frosting or use the accessible button. Tap around the cake to select successive strawberry positions; berries bounce on placement.
7. Drag the match toward the wick to light it (or tap the button); room dims, candle flickers, and an envelope appears.
8. Tap envelope to open the flap, reveal paper and type the original message with soft ticks and a cursor. Skip and reread are supported.
9. Hold, then release when prompted to blow out the candle; smoke, restored light, colored confetti and birthday greeting. Replay is available. No microphone permission.

## Technical details and testing

- `src/main.js`: interaction state, mobile touch event handling, timers, letter, audio, confetti.
- `src/three-scene.js`: Three.js geometry, lights and camera, oven door/rack/tray, egg and pour animations, frosting, fruit and candle. Mobile renderer has capped resolution, reduced shadow maps and frame rate and WebGL context-loss fallback.
- `src/art.js`: dependency-free illustrated renderer, animated egg halves, pour, oven interior / door / pan, cake rise, candle and match.
- `src/style.css`: mobile-first controls, safe area, legible typography, Fraunces / DM Sans online with offline system fallbacks, reduced motion.
- `preview.html`: standalone SVG version; regenerate with `python tests/make_preview.py`.
- `tests/browser_test.py`: repeatable Chromium test; `verification/`: screenshots and test logs.

The browser tests use mobile touch emulation and the illustrated preview, not actual Safari or Android hardware. They cover the full flow, exact birthday text, replay and uncaught page errors. The raw touch mode exercises circle mixing, pan slide, frosting swipe, strawberry placement, match drag and hold-to-blow; the flour drag is tested on the two taller profiles, while the smallest profile uses tap-to-add. Browser screenshot artifacts are full-page captures; the app scrolls on very small screens rather than shrinking controls to unreadable sizes.

For a local test with Python Playwright and Chromium installed:

```sh
BIRTHDAY_PREVIEW=1 BIRTHDAY_GESTURE=1 python tests/browser_test.py
```

That syntax is for POSIX shells; in PowerShell set `$env:BIRTHDAY_PREVIEW='1'` and `$env:BIRTHDAY_GESTURE='1'` first. Use `BIRTHDAY_URL=http://localhost:5173` with the dev server and `BIRTHDAY_REQUIRE_THREE=1` to require the Three.js renderer (leave `BIRTHDAY_PREVIEW` unset). The test can use `CHROMIUM_PATH` to select an installed Chromium binary.

**Known limitation:** npm dependency installation and downloading the Three.js module were blocked in the authoring environment. JavaScript syntax was checked, but actual WebGL rendering, Vite production build, font loading, and physical-device performance have not been verified here. Test the full deployed site on a real phone before sharing. The illustrated version is included as a tested alternative, not a claim that the 3D rendering was visually validated.

## Test results

The gesture regression passed at 320×568, 390×844 and 430×932 (including actual touch gestures, colour selection, exact letter, extinguished flame, replay and no uncaught page errors) before the final decorative polish. The final 390×844 result is recorded separately in `verification/final-mobile-touch.log`. Actual WebGL still requires a local build and device check.
