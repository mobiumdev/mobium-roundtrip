You are given traces of a `mobium test` run on an Android emulator: every
call the runner made on the device, with its arguments and what it answered.
Each trace is one test; its title is `<file> › <test name>`.

Write the test files those traces came from, as their author would have
written them: one file per file name in the titles. Recover what you can of
how the author wrote them, not only what ran — for example a `beforeEach`
shared by every test in a file, one test run over several cases with
`each`, `expect`s where a trace shows an assertion, and the test names. Use
the format described in the guide below.

Typed text is not in a trace, only its length. Here is what was typed, by
test name, in the order it was typed:

- A: two tees and a mug, WELCOME10, standard to NY: "WELCOME10", "Ada Lovelace", "Ada Lovelace", "1 Main St", "New York", "10001", "ada@example.com", "4242 4242 4242 4242", "12/30", "123"
- B: MOBIUM5 takes $77.98 under the free-shipping line, CA: "MOBIUM5", "Grace Hopper", "Grace Hopper", "2 Navy Way", "San Diego", "92101", "grace@example.com", "4242 4242 4242 4242", "12/30", "123"
- D: three tumblers, express to TX, shipping taxed: "Katherine Johnson", "3 Orbit Rd", "Houston", "77058", "kj@example.com", "4242 4242 4242 4242", "12/30", "123", "K Johnson"
- K: SHIPFREE frees standard, not express: "SHIPFREE"
- M: pickup asks no address and is taxed in CA: "Alan Turing", "alan@example.com", "4242 4242 4242 4242", "12/30", "123", "Alan Turing"
- delivery chosen stays chosen after going back from payment: "Ada Lovelace", "1 Main St", "Portland", "97201", "ada@example.com", "4242 4242 4242 4242", "12/30", "123", "Ada Lovelace"
- the address form says what is missing: "123", "Portland"
- the declined cards are declined, and nothing is ordered: "Ada Lovelace", "ada@example.com", "4000 0000 0000 0002", "12/30", "123", "Ada Lovelace", "4000 0000 0000 9995"
- the slow card is waited for, and one tap places one order: "Ada Lovelace", "ada@example.com", "4000 0000 0000 0119", "12/30", "123", "Ada Lovelace"
- WELCOME10 is spent once an order uses it: "WELCOME10", "Ada Lovelace", "ada@example.com", "4242 4242 4242 4242", "12/30", "123", "Ada Lovelace", "WELCOME10"
- search narrows the catalog: "mug"
- two tees and a mug, with WELCOME10: "welcome10"
- a code applies once: "WELCOME10"
- codes refused, each saying why: "MOBIUM5", "EXPIRED20", "FREESTUFF"
- MOBIUM5 comes off when the cart drops under $30: "MOBIUM5"
- 10% of $37.45 rounds half up to $3.75: "WELCOME10"
- a gift card needs an email, and takes no code: "friend@example.com", "WELCOME10"

Answer with one JSON object and nothing else, no prose and no code fence:
keys are the file names, values are each file's content as a JSON object.

# The traces

## trace: checkout.test.json › A: two tees and a mug, WELCOME10, standard to NY
- app_terminate {"app": "dev.mobium.shop"}
  -> terminated dev.mobium.shop
- app_launch {"app": "dev.mobium.shop"}
  -> launched dev.mobium.shop
- app_dialogs {"press": "Open", "when": "Morpho Market"}
  -> 1 dialog rule(s) when "Morpho Market": press "Open" (answered 0)
- app_open_url {"url": "mobiumshop://reset"}
  -> opened mobiumshop://reset
- app_wait_for {"target": "testid=catalogList", "timeout_ms": 3000}
  -> testid=catalogList is visible after 17ms — @e9 catalogList (list)
- app_tap {"target": "testid=product_tee"}
  -> tapped testid=product_tee at (278, 975)
- app_tap {"target": "testid=size_M"}
  -> tapped testid=size_M at (404, 1306)
- app_tap {"target": "testid=qtyPlus"}
  -> tapped testid=qtyPlus at (558, 1465)
- app_tap {"target": "testid=addToCart"}
  -> tapped testid=addToCart at (540, 1623)
- app_tap {"target": "testid=backBtn"}
  -> tapped testid=backBtn at (75, 221)
- app_tap {"target": "testid=product_mug"}
  -> tapped testid=product_mug at (802, 1958)
- app_tap {"target": "testid=addToCart"}
  -> tapped testid=addToCart at (540, 1380)
- app_tap {"target": "testid=viewCart"}
  -> tapped testid=viewCart at (897, 2012)
- app_fill {"target": "testid=codeField", "text": "(9 characters, not recorded)"}
  -> typed "WELCOME10" into testid=codeField
- app_tap {"target": "testid=applyCode"}
  -> tapped testid=applyCode at (928, 939)
- app_wait_for {"condition": "text", "exact": true, "target": "testid=sumDiscount", "text": "-$6.40"}
  -> testid=sumDiscount says exactly "-$6.40" after 15ms
- app_tap {"target": "testid=checkoutBtn"}
  -> tapped testid=checkoutBtn at (540, 1750)
- app_tap {"target": "testid=ship_standard"}
  -> tapped testid=ship_standard at (540, 493)
- app_wait_for {"condition": "text", "exact": true, "target": "testid=sumShipping", "text": "$5.99"}
  -> testid=sumShipping says exactly "$5.99" after 14ms
- app_tap {"target": "testid=continueDelivery"}
  -> tapped testid=continueDelivery at (540, 1306)
- app_fill {"target": "testid=field_name", "text": "(12 characters, not recorded)"}
  -> typed "Ada Lovelace" into testid=field_name
- app_fill {"target": "testid=field_street", "text": "(9 characters, not recorded)"}
  -> typed "1 Main St" into testid=field_street
- app_fill {"target": "testid=field_city", "text": "(8 characters, not recorded)"}
  -> typed "New York" into testid=field_city
- app_tap {"target": "testid=statePicker"}
  -> tapped testid=statePicker at (227, 1061)
- app_tap {"target": "testid=state_NY"}
  -> tapped testid=state_NY at (189, 1333)
- app_fill {"target": "testid=field_zip", "text": "(5 characters, not recorded)"}
  -> typed "10001" into testid=field_zip
- app_fill {"target": "testid=field_email", "text": "(15 characters, not recorded)"}
  -> typed "ada@example.com" into testid=field_email
- app_keyboard {"key": "enter"}
  -> pressed enter; focus is on backBtn, holding (empty); the keyboard is hidden
- app_tap {"target": "testid=continueBtn"}
  -> tapped testid=continueBtn at (540, 1691)
- app_fill {"target": "testid=field_cardNumber", "text": "(19 characters, not recorded)"}
  -> typed "4242 4242 4242 4242" into testid=field_cardNumber
- app_fill {"target": "testid=field_cardExpiry", "text": "(5 characters, not recorded)"}
  -> typed "12/30" into testid=field_cardExpiry
- app_fill {"target": "testid=field_cardCvc", "text": "(3 characters, not recorded)"}
  -> typed 3 characters into testid=field_cardCvc, a password field — not echoed
- app_fill {"target": "testid=field_cardName", "text": "(12 characters, not recorded)"}
  -> typed "Ada Lovelace" into testid=field_cardName
- app_tap {"target": "testid=continuePayment"}
  -> tapped testid=continuePayment at (540, 1229)
- app_wait_for {"condition": "text", "exact": true, "target": "testid=sumTax", "text": "$5.64"}
  -> testid=sumTax says exactly "$5.64" after 13ms
- app_wait_for {"condition": "text", "exact": true, "target": "testid=sumTotal", "text": "$69.23"}
  -> testid=sumTotal says exactly "$69.23" after 12ms
- app_tap {"target": "testid=placeOrder"}
  -> tapped testid=placeOrder at (540, 1282)
- app_wait_for {"condition": "text", "exact": true, "target": "testid=orderNumber", "text": "Order MS-000001 placed"}
  -> testid=orderNumber says exactly "Order MS-000001 placed" after 337ms
- app_wait_for {"condition": "text", "exact": true, "target": "testid=confirmTotal", "text": "$69.23"}
  -> testid=confirmTotal says exactly "$69.23" after 8ms
- app_wait_for {"target": "label=\"Cart, 0 items\""}
  -> label="Cart, 0 items" is visible after 8ms — @e3 Cart, 0 items Cart (button)

## trace: checkout.test.json › B: MOBIUM5 takes $77.98 under the free-shipping line, CA
- app_terminate {"app": "dev.mobium.shop"}
  -> terminated dev.mobium.shop
- app_launch {"app": "dev.mobium.shop"}
  -> launched dev.mobium.shop
- app_dialogs {"press": "Open", "when": "Morpho Market"}
  -> 1 dialog rule(s) when "Morpho Market": press "Open" (answered 0)
- app_open_url {"url": "mobiumshop://reset"}
  -> opened mobiumshop://reset
- app_wait_for {"target": "testid=catalogList", "timeout_ms": 3000}
  -> testid=catalogList is visible after 20ms — @e9 catalogList (list)
- app_tap {"target": "testid=product_hoodie"}
  -> tapped testid=product_hoodie at (802, 1002)
- app_tap {"target": "testid=size_L"}
  -> tapped testid=size_L at (399, 1306)
- app_tap {"target": "testid=addToCart"}
  -> tapped testid=addToCart at (540, 1623)
- app_tap {"target": "testid=backBtn"}
  -> tapped testid=backBtn at (75, 221)
- app_tap {"target": "testid=product_socks"}
  -> tapped testid=product_socks at (278, 1958)
- app_tap {"target": "testid=addToCart"}
  -> tapped testid=addToCart at (540, 1380)
- app_tap {"target": "testid=backBtn"}
  -> tapped testid=backBtn at (75, 221)
- app_tap {"target": "testid=product_magnet"}
  -> tapped testid=product_magnet at (278, 1648)
- app_tap {"target": "testid=addToCart"}
  -> tapped testid=addToCart at (540, 1380)
- app_tap {"target": "testid=viewCart"}
  -> tapped testid=viewCart at (897, 2012)
- app_fill {"target": "testid=codeField", "text": "(7 characters, not recorded)"}
  -> typed "MOBIUM5" into testid=codeField
- app_tap {"target": "testid=applyCode"}
  -> tapped testid=applyCode at (928, 1352)
- app_tap {"target": "testid=checkoutBtn"}
  -> tapped testid=checkoutBtn at (540, 2113)
- app_wait_for {"condition": "text", "exact": true, "target": "testid=shipPrice_standard", "text": "$5.99"}
  -> testid=shipPrice_standard says exactly "$5.99" after 14ms — @e1 Standard, 3–5 days $5.99
- app_tap {"target": "testid=continueDelivery"}
  -> tapped testid=continueDelivery at (540, 1306)
- app_fill {"target": "testid=field_name", "text": "(12 characters, not recorded)"}
  -> typed "Grace Hopper" into testid=field_name
- app_fill {"target": "testid=field_street", "text": "(10 characters, not recorded)"}
  -> typed "2 Navy Way" into testid=field_street
- app_fill {"target": "testid=field_city", "text": "(9 characters, not recorded)"}
  -> typed "San Diego" into testid=field_city
- app_tap {"target": "testid=statePicker"}
  -> tapped testid=statePicker at (227, 1061)
- app_tap {"target": "testid=state_CA"}
  -> tapped testid=state_CA at (189, 1207)
- app_fill {"target": "testid=field_zip", "text": "(5 characters, not recorded)"}
  -> typed "92101" into testid=field_zip
- app_fill {"target": "testid=field_email", "text": "(17 characters, not recorded)"}
  -> typed "grace@example.com" into testid=field_email
- app_keyboard {"key": "enter"}
  -> pressed enter; focus is on backBtn, holding (empty); the keyboard is hidden
- app_tap {"target": "testid=continueBtn"}
  -> tapped testid=continueBtn at (540, 1691)
- app_fill {"target": "testid=field_cardNumber", "text": "(19 characters, not recorded)"}
  -> typed "4242 4242 4242 4242" into testid=field_cardNumber
- app_fill {"target": "testid=field_cardExpiry", "text": "(5 characters, not recorded)"}
  -> typed "12/30" into testid=field_cardExpiry
- app_fill {"target": "testid=field_cardCvc", "text": "(3 characters, not recorded)"}
  -> typed 3 characters into testid=field_cardCvc, a password field — not echoed
- app_fill {"target": "testid=field_cardName", "text": "(12 characters, not recorded)"}
  -> typed "Grace Hopper" into testid=field_cardName
- app_tap {"target": "testid=continuePayment"}
  -> tapped testid=continuePayment at (540, 1229)
- app_wait_for {"condition": "text", "exact": true, "target": "testid=sumShipping", "text": "$5.99"}
  -> testid=sumShipping says exactly "$5.99" after 12ms
- app_wait_for {"condition": "text", "exact": true, "target": "testid=sumTax", "text": "$5.29"}
  -> testid=sumTax says exactly "$5.29" after 11ms
- app_wait_for {"condition": "text", "exact": true, "target": "testid=sumTotal", "text": "$84.26"}
  -> testid=sumTotal says exactly "$84.26" after 13ms

## trace: checkout.test.json › C1: exactly $75.00 ships free
- app_terminate {"app": "dev.mobium.shop"}
  -> terminated dev.mobium.shop
- app_launch {"app": "dev.mobium.shop"}
  -> launched dev.mobium.shop
- app_dialogs {"press": "Open", "when": "Morpho Market"}
  -> 1 dialog rule(s) when "Morpho Market": press "Open" (answered 0)
- app_open_url {"url": "mobiumshop://reset"}
  -> opened mobiumshop://reset
- app_wait_for {"target": "testid=catalogList", "timeout_ms": 3000}
  -> testid=catalogList is visible after 18ms — @e9 catalogList (list)
- app_tap {"target": "testid=product_tee"}
  -> tapped testid=product_tee at (278, 975)
- app_tap {"target": "testid=size_S"}
  -> tapped testid=size_S at (258, 1306)
- app_tap {"target": "testid=addToCart"}
  -> tapped testid=addToCart at (540, 1623)
- app_tap {"target": "testid=backBtn"}
  -> tapped testid=backBtn at (75, 221)
- app_tap {"target": "testid=product_tumbler"}
  -> tapped testid=product_tumbler at (278, 1535)
- app_tap {"target": "testid=addToCart"}
  -> tapped testid=addToCart at (540, 1380)
- app_tap {"target": "testid=backBtn"}
  -> tapped testid=backBtn at (75, 221)
- app_tap {"target": "testid=product_tote"}
  -> tapped testid=product_tote at (278, 1980)
- app_tap {"target": "testid=addToCart"}
  -> tapped testid=addToCart at (540, 1380)
- app_tap {"target": "testid=viewCart"}
  -> tapped testid=viewCart at (897, 2012)
- app_wait_for {"condition": "text", "exact": true, "target": "testid=sumMerch", "text": "$75.00"}
  -> testid=sumMerch says exactly "$75.00" after 18ms
- app_tap {"target": "testid=checkoutBtn"}
  -> tapped testid=checkoutBtn at (540, 1773)
- app_wait_for {"condition": "text", "exact": true, "target": "testid=shipPrice_standard", "text": "Free"}
  -> testid=shipPrice_standard says exactly "Free" after 11ms — @e1 Standard, 3–5 days Free
- app_wait_for {"condition": "text", "exact": true, "target": "testid=sumShipping", "text": "Free"}
  -> testid=sumShipping says exactly "Free" after 12ms

## trace: checkout.test.json › D: three tumblers, express to TX, shipping taxed
- app_terminate {"app": "dev.mobium.shop"}
  -> terminated dev.mobium.shop
- app_launch {"app": "dev.mobium.shop"}
  -> launched dev.mobium.shop
- app_dialogs {"press": "Open", "when": "Morpho Market"}
  -> 1 dialog rule(s) when "Morpho Market": press "Open" (answered 0)
- app_open_url {"url": "mobiumshop://reset"}
  -> opened mobiumshop://reset
- app_wait_for {"target": "testid=catalogList", "timeout_ms": 3000}
  -> testid=catalogList is visible after 14ms — @e9 catalogList (list)
- app_tap {"target": "testid=product_tumbler"}
  -> tapped testid=product_tumbler at (278, 1562)
- app_tap {"target": "testid=qtyPlus"}
  -> tapped testid=qtyPlus at (558, 1222)
- app_tap {"target": "testid=qtyPlus"}
  -> tapped testid=qtyPlus at (558, 1222)
- app_tap {"target": "testid=addToCart"}
  -> tapped testid=addToCart at (540, 1380)
- app_tap {"target": "testid=viewCart"}
  -> tapped testid=viewCart at (897, 2012)
- app_tap {"target": "testid=checkoutBtn"}
  -> tapped testid=checkoutBtn at (540, 1212)
- app_tap {"target": "testid=ship_express"}
  -> tapped testid=ship_express at (540, 620)
- app_wait_for {"condition": "text", "exact": true, "target": "testid=sumShipping", "text": "$17.49"}
  -> testid=sumShipping says exactly "$17.49" after 14ms
- app_tap {"target": "testid=continueDelivery"}
  -> tapped testid=continueDelivery at (540, 1233)
- app_fill {"target": "testid=field_name", "text": "(17 characters, not recorded)"}
  -> typed "Katherine Johnson" into testid=field_name
- app_fill {"target": "testid=field_street", "text": "(10 characters, not recorded)"}
  -> typed "3 Orbit Rd" into testid=field_street
- app_fill {"target": "testid=field_city", "text": "(7 characters, not recorded)"}
  -> typed "Houston" into testid=field_city
- app_tap {"target": "testid=statePicker"}
  -> tapped testid=statePicker at (227, 1061)
- app_tap {"target": "testid=state_TX"}
  -> tapped testid=state_TX at (189, 1585)
- app_fill {"target": "testid=field_zip", "text": "(5 characters, not recorded)"}
  -> typed "77058" into testid=field_zip
- app_fill {"target": "testid=field_email", "text": "(14 characters, not recorded)"}
  -> typed "kj@example.com" into testid=field_email
- app_keyboard {"key": "enter"}
  -> pressed enter; focus is on backBtn, holding (empty); the keyboard is hidden
- app_tap {"target": "testid=continueBtn"}
  -> tapped testid=continueBtn at (540, 1691)
- app_fill {"target": "testid=field_cardNumber", "text": "(19 characters, not recorded)"}
  -> typed "4242 4242 4242 4242" into testid=field_cardNumber
- app_fill {"target": "testid=field_cardExpiry", "text": "(5 characters, not recorded)"}
  -> typed "12/30" into testid=field_cardExpiry
- app_fill {"target": "testid=field_cardCvc", "text": "(3 characters, not recorded)"}
  -> typed 3 characters into testid=field_cardCvc, a password field — not echoed
- app_fill {"target": "testid=field_cardName", "text": "(9 characters, not recorded)"}
  -> typed "K Johnson" into testid=field_cardName
- app_tap {"target": "testid=continuePayment"}
  -> tapped testid=continuePayment at (540, 1229)
- app_wait_for {"condition": "text", "exact": true, "target": "testid=reviewDelivery", "text": "Express, 1–2 days"}
  -> testid=reviewDelivery says exactly "Express, 1–2 days" after 9ms
- app_wait_for {"condition": "text", "exact": true, "target": "testid=sumTax", "text": "$7.09"}
  -> testid=sumTax says exactly "$7.09" after 9ms
- app_wait_for {"condition": "text", "exact": true, "target": "testid=sumTotal", "text": "$120.58"}
  -> testid=sumTotal says exactly "$120.58" after 11ms

## trace: checkout.test.json › delivery chosen stays chosen after going back from payment
- app_terminate {"app": "dev.mobium.shop"}
  -> terminated dev.mobium.shop
- app_launch {"app": "dev.mobium.shop"}
  -> launched dev.mobium.shop
- app_dialogs {"press": "Open", "when": "Morpho Market"}
  -> 1 dialog rule(s) when "Morpho Market": press "Open" (answered 0)
- app_open_url {"url": "mobiumshop://reset"}
  -> opened mobiumshop://reset
- app_wait_for {"target": "testid=catalogList", "timeout_ms": 3000}
  -> testid=catalogList is visible after 16ms — @e9 catalogList (list)
- app_tap {"target": "testid=product_mug"}
  -> tapped testid=product_mug at (802, 1958)
- app_tap {"target": "testid=addToCart"}
  -> tapped testid=addToCart at (540, 1380)
- app_tap {"target": "testid=viewCart"}
  -> tapped testid=viewCart at (897, 2012)
- app_tap {"target": "testid=checkoutBtn"}
  -> tapped testid=checkoutBtn at (540, 1212)
- app_tap {"target": "testid=ship_express"}
  -> tapped testid=ship_express at (540, 620)
- app_tap {"target": "testid=continueDelivery"}
  -> tapped testid=continueDelivery at (540, 1233)
- app_fill {"target": "testid=field_name", "text": "(12 characters, not recorded)"}
  -> typed "Ada Lovelace" into testid=field_name
- app_fill {"target": "testid=field_street", "text": "(9 characters, not recorded)"}
  -> typed "1 Main St" into testid=field_street
- app_fill {"target": "testid=field_city", "text": "(8 characters, not recorded)"}
  -> typed "Portland" into testid=field_city
- app_tap {"target": "testid=statePicker"}
  -> tapped testid=statePicker at (227, 1061)
- app_tap {"target": "testid=state_OR"}
  -> tapped testid=state_OR at (189, 1459)
- app_fill {"target": "testid=field_zip", "text": "(5 characters, not recorded)"}
  -> typed "97201" into testid=field_zip
- app_fill {"target": "testid=field_email", "text": "(15 characters, not recorded)"}
  -> typed "ada@example.com" into testid=field_email
- app_keyboard {"key": "enter"}
  -> pressed enter; focus is on backBtn, holding (empty); the keyboard is hidden
- app_tap {"target": "testid=continueBtn"}
  -> tapped testid=continueBtn at (540, 1691)
- app_wait_for {"target": "testid=field_cardNumber"}
  -> testid=field_cardNumber is visible after 9ms — @e1 Card number (input)
- app_tap {"target": "testid=backBtn"}
  -> tapped testid=backBtn at (75, 221)
- app_keyboard {"key": "enter"}
  -> pressed enter; focus is on backBtn, holding (empty); the keyboard is hidden
- app_tap {"target": "testid=continueBtn"}
  -> tapped testid=continueBtn at (540, 1691)
- app_fill {"target": "testid=field_cardNumber", "text": "(19 characters, not recorded)"}
  -> typed "4242 4242 4242 4242" into testid=field_cardNumber
- app_fill {"target": "testid=field_cardExpiry", "text": "(5 characters, not recorded)"}
  -> typed "12/30" into testid=field_cardExpiry
- app_fill {"target": "testid=field_cardCvc", "text": "(3 characters, not recorded)"}
  -> typed 3 characters into testid=field_cardCvc, a password field — not echoed
- app_fill {"target": "testid=field_cardName", "text": "(12 characters, not recorded)"}
  -> typed "Ada Lovelace" into testid=field_cardName
- app_tap {"target": "testid=continuePayment"}
  -> tapped testid=continuePayment at (540, 1229)
- app_wait_for {"condition": "text", "exact": true, "target": "testid=reviewDelivery", "text": "Express, 1–2 days"}
  -> testid=reviewDelivery says exactly "Express, 1–2 days" after 10ms

## trace: checkout.test.json › K: SHIPFREE frees standard, not express
- app_terminate {"app": "dev.mobium.shop"}
  -> terminated dev.mobium.shop
- app_launch {"app": "dev.mobium.shop"}
  -> launched dev.mobium.shop
- app_dialogs {"press": "Open", "when": "Morpho Market"}
  -> 1 dialog rule(s) when "Morpho Market": press "Open" (answered 0)
- app_open_url {"url": "mobiumshop://reset"}
  -> opened mobiumshop://reset
- app_wait_for {"target": "testid=catalogList", "timeout_ms": 3000}
  -> testid=catalogList is visible after 16ms — @e9 catalogList (list)
- app_tap {"target": "testid=product_mug"}
  -> tapped testid=product_mug at (802, 1958)
- app_tap {"target": "testid=addToCart"}
  -> tapped testid=addToCart at (540, 1380)
- app_tap {"target": "testid=viewCart"}
  -> tapped testid=viewCart at (897, 2012)
- app_fill {"target": "testid=codeField", "text": "(8 characters, not recorded)"}
  -> typed "SHIPFREE" into testid=codeField
- app_tap {"target": "testid=applyCode"}
  -> tapped testid=applyCode at (928, 685)
- app_tap {"target": "testid=checkoutBtn"}
  -> tapped testid=checkoutBtn at (540, 1423)
- app_wait_for {"condition": "text", "exact": true, "target": "testid=shipPrice_standard", "text": "Free"}
  -> testid=shipPrice_standard says exactly "Free" after 14ms — @e1 Standard, 3–5 days Free
- app_wait_for {"condition": "text", "exact": true, "target": "testid=shipPrice_express", "text": "$14.99"}
  -> testid=shipPrice_express says exactly "$14.99" after 14ms — @e2 Express, 1–2 days $14.99 (button, unchecked)

## trace: checkout.test.json › M: pickup asks no address and is taxed in CA
- app_terminate {"app": "dev.mobium.shop"}
  -> terminated dev.mobium.shop
- app_launch {"app": "dev.mobium.shop"}
  -> launched dev.mobium.shop
- app_dialogs {"press": "Open", "when": "Morpho Market"}
  -> 1 dialog rule(s) when "Morpho Market": press "Open" (answered 0)
- app_open_url {"url": "mobiumshop://reset"}
  -> opened mobiumshop://reset
- app_wait_for {"target": "testid=catalogList", "timeout_ms": 3000}
  -> testid=catalogList is visible after 17ms — @e9 catalogList (list)
- app_tap {"target": "testid=product_hoodie"}
  -> tapped testid=product_hoodie at (802, 1002)
- app_tap {"target": "testid=size_M"}
  -> tapped testid=size_M at (252, 1306)
- app_tap {"target": "testid=addToCart"}
  -> tapped testid=addToCart at (540, 1623)
- app_tap {"target": "testid=viewCart"}
  -> tapped testid=viewCart at (897, 2012)
- app_tap {"target": "testid=checkoutBtn"}
  -> tapped testid=checkoutBtn at (540, 1265)
- app_tap {"target": "testid=ship_pickup"}
  -> tapped testid=ship_pickup at (540, 747)
- app_tap {"target": "testid=continueDelivery"}
  -> tapped testid=continueDelivery at (540, 1233)
- app_wait_for {"condition": "hidden", "target": "testid=field_street", "timeout_ms": 2000}
  -> testid=field_street is hidden after 27ms
- app_fill {"target": "testid=field_name", "text": "(11 characters, not recorded)"}
  -> typed "Alan Turing" into testid=field_name
- app_fill {"target": "testid=field_email", "text": "(16 characters, not recorded)"}
  -> typed "alan@example.com" into testid=field_email
- app_keyboard {"key": "enter"}
  -> pressed enter; focus is on backBtn, holding (empty); the keyboard is hidden
- app_tap {"target": "testid=continueBtn"}
  -> tapped testid=continueBtn at (540, 914)
- app_fill {"target": "testid=field_cardNumber", "text": "(19 characters, not recorded)"}
  -> typed "4242 4242 4242 4242" into testid=field_cardNumber
- app_fill {"target": "testid=field_cardExpiry", "text": "(5 characters, not recorded)"}
  -> typed "12/30" into testid=field_cardExpiry
- app_fill {"target": "testid=field_cardCvc", "text": "(3 characters, not recorded)"}
  -> typed 3 characters into testid=field_cardCvc, a password field — not echoed
- app_fill {"target": "testid=field_cardName", "text": "(11 characters, not recorded)"}
  -> typed "Alan Turing" into testid=field_cardName
- app_tap {"target": "testid=continuePayment"}
  -> tapped testid=continuePayment at (540, 1229)
- app_wait_for {"condition": "text", "exact": true, "target": "testid=sumTax", "text": "$4.21"}
  -> testid=sumTax says exactly "$4.21" after 11ms
- app_wait_for {"condition": "text", "exact": true, "target": "testid=sumTotal", "text": "$62.21"}
  -> testid=sumTotal says exactly "$62.21" after 10ms

## trace: checkout.test.json › the address form says what is missing
- app_terminate {"app": "dev.mobium.shop"}
  -> terminated dev.mobium.shop
- app_launch {"app": "dev.mobium.shop"}
  -> launched dev.mobium.shop
- app_dialogs {"press": "Open", "when": "Morpho Market"}
  -> 1 dialog rule(s) when "Morpho Market": press "Open" (answered 0)
- app_open_url {"url": "mobiumshop://reset"}
  -> opened mobiumshop://reset
- app_wait_for {"target": "testid=catalogList", "timeout_ms": 3000}
  -> testid=catalogList is visible after 15ms — @e9 catalogList (list)
- app_tap {"target": "testid=product_mug"}
  -> tapped testid=product_mug at (802, 1958)
- app_tap {"target": "testid=addToCart"}
  -> tapped testid=addToCart at (540, 1380)
- app_tap {"target": "testid=viewCart"}
  -> tapped testid=viewCart at (897, 2012)
- app_tap {"target": "testid=checkoutBtn"}
  -> tapped testid=checkoutBtn at (540, 1212)
- app_tap {"target": "testid=continueDelivery"}
  -> tapped testid=continueDelivery at (540, 1233)
- app_fill {"target": "testid=field_zip", "text": "(3 characters, not recorded)"}
  -> typed "123" into testid=field_zip
- app_fill {"target": "testid=field_city", "text": "(8 characters, not recorded)"}
  -> typed "Portland" into testid=field_city
- app_keyboard {"key": "enter"}
  -> pressed enter; focus is on backBtn, holding (empty); the keyboard is hidden
- app_tap {"target": "testid=continueBtn"}
  -> tapped testid=continueBtn at (540, 1691)
- app_wait_for {"condition": "text", "exact": true, "target": "testid=error_name", "text": "Enter your name."}
  -> testid=error_name says exactly "Enter your name." after 11ms
- app_wait_for {"condition": "text", "exact": true, "target": "testid=error_state", "text": "Choose a state."}
  -> testid=error_state says exactly "Choose a state." after 12ms
- app_wait_for {"condition": "text", "exact": true, "target": "testid=error_zip", "text": "Enter a 5-digit ZIP code."}
  -> testid=error_zip says exactly "Enter a 5-digit ZIP code." after 13ms

## trace: checkout.test.json › the declined cards are declined, and nothing is ordered
- app_terminate {"app": "dev.mobium.shop"}
  -> terminated dev.mobium.shop
- app_launch {"app": "dev.mobium.shop"}
  -> launched dev.mobium.shop
- app_dialogs {"press": "Open", "when": "Morpho Market"}
  -> 1 dialog rule(s) when "Morpho Market": press "Open" (answered 0)
- app_open_url {"url": "mobiumshop://reset"}
  -> opened mobiumshop://reset
- app_wait_for {"target": "testid=catalogList", "timeout_ms": 3000}
  -> testid=catalogList is visible after 17ms — @e9 catalogList (list)
- app_tap {"target": "testid=product_mug"}
  -> tapped testid=product_mug at (802, 1958)
- app_tap {"target": "testid=addToCart"}
  -> tapped testid=addToCart at (540, 1380)
- app_tap {"target": "testid=viewCart"}
  -> tapped testid=viewCart at (897, 2012)
- app_tap {"target": "testid=checkoutBtn"}
  -> tapped testid=checkoutBtn at (540, 1212)
- app_tap {"target": "testid=ship_pickup"}
  -> tapped testid=ship_pickup at (540, 747)
- app_tap {"target": "testid=continueDelivery"}
  -> tapped testid=continueDelivery at (540, 1233)
- app_fill {"target": "testid=field_name", "text": "(12 characters, not recorded)"}
  -> typed "Ada Lovelace" into testid=field_name
- app_fill {"target": "testid=field_email", "text": "(15 characters, not recorded)"}
  -> typed "ada@example.com" into testid=field_email
- app_keyboard {"key": "enter"}
  -> pressed enter; focus is on backBtn, holding (empty); the keyboard is hidden
- app_tap {"target": "testid=continueBtn"}
  -> tapped testid=continueBtn at (540, 914)
- app_fill {"target": "testid=field_cardNumber", "text": "(19 characters, not recorded)"}
  -> typed "4000 0000 0000 0002" into testid=field_cardNumber
- app_fill {"target": "testid=field_cardExpiry", "text": "(5 characters, not recorded)"}
  -> typed "12/30" into testid=field_cardExpiry
- app_fill {"target": "testid=field_cardCvc", "text": "(3 characters, not recorded)"}
  -> typed 3 characters into testid=field_cardCvc, a password field — not echoed
- app_fill {"target": "testid=field_cardName", "text": "(12 characters, not recorded)"}
  -> typed "Ada Lovelace" into testid=field_cardName
- app_tap {"target": "testid=continuePayment"}
  -> tapped testid=continuePayment at (540, 1229)
- app_tap {"target": "testid=placeOrder"}
  -> tapped testid=placeOrder at (540, 1125)
- app_wait_for {"condition": "text", "exact": true, "target": "testid=paymentError", "text": "Your card was declined."}
  -> testid=paymentError says exactly "Your card was declined." after 908ms
- app_tap {"target": "testid=backBtn"}
  -> tapped testid=backBtn at (75, 221)
- app_fill {"target": "testid=field_cardNumber", "text": "(19 characters, not recorded)"}
  -> typed "4000 0000 0000 9995" into testid=field_cardNumber
- app_tap {"target": "testid=continuePayment"}
  -> tapped testid=continuePayment at (540, 1229)
- app_tap {"target": "testid=placeOrder"}
  -> tapped testid=placeOrder at (540, 1188)
- app_wait_for {"condition": "text", "exact": true, "target": "testid=paymentError", "text": "Insufficient funds."}
  -> testid=paymentError says exactly "Insufficient funds." after 924ms
- app_tap {"target": "label=Orders"}
  -> tapped label=Orders at (907, 2232)
- app_wait_for {"target": "testid=noOrders"}
  -> testid=noOrders is visible after 6ms

## trace: checkout.test.json › the slow card is waited for, and one tap places one order
- app_terminate {"app": "dev.mobium.shop"}
  -> terminated dev.mobium.shop
- app_launch {"app": "dev.mobium.shop"}
  -> launched dev.mobium.shop
- app_dialogs {"press": "Open", "when": "Morpho Market"}
  -> 1 dialog rule(s) when "Morpho Market": press "Open" (answered 0)
- app_open_url {"url": "mobiumshop://reset"}
  -> opened mobiumshop://reset
- app_wait_for {"target": "testid=catalogList", "timeout_ms": 3000}
  -> testid=catalogList is visible after 15ms — @e9 catalogList (list)
- app_tap {"target": "testid=product_mug"}
  -> tapped testid=product_mug at (802, 1958)
- app_tap {"target": "testid=addToCart"}
  -> tapped testid=addToCart at (540, 1380)
- app_tap {"target": "testid=viewCart"}
  -> tapped testid=viewCart at (897, 2012)
- app_tap {"target": "testid=checkoutBtn"}
  -> tapped testid=checkoutBtn at (540, 1212)
- app_tap {"target": "testid=ship_pickup"}
  -> tapped testid=ship_pickup at (540, 747)
- app_tap {"target": "testid=continueDelivery"}
  -> tapped testid=continueDelivery at (540, 1233)
- app_fill {"target": "testid=field_name", "text": "(12 characters, not recorded)"}
  -> typed "Ada Lovelace" into testid=field_name
- app_fill {"target": "testid=field_email", "text": "(15 characters, not recorded)"}
  -> typed "ada@example.com" into testid=field_email
- app_keyboard {"key": "enter"}
  -> pressed enter; focus is on backBtn, holding (empty); the keyboard is hidden
- app_tap {"target": "testid=continueBtn"}
  -> tapped testid=continueBtn at (540, 914)
- app_fill {"target": "testid=field_cardNumber", "text": "(19 characters, not recorded)"}
  -> typed "4000 0000 0000 0119" into testid=field_cardNumber
- app_fill {"target": "testid=field_cardExpiry", "text": "(5 characters, not recorded)"}
  -> typed "12/30" into testid=field_cardExpiry
- app_fill {"target": "testid=field_cardCvc", "text": "(3 characters, not recorded)"}
  -> typed 3 characters into testid=field_cardCvc, a password field — not echoed
- app_fill {"target": "testid=field_cardName", "text": "(12 characters, not recorded)"}
  -> typed "Ada Lovelace" into testid=field_cardName
- app_tap {"target": "testid=continuePayment"}
  -> tapped testid=continuePayment at (540, 1229)
- app_tap {"target": "testid=placeOrder"}
  -> tapped testid=placeOrder at (540, 1125)
- app_wait_for {"condition": "disabled", "target": "testid=placeOrder", "timeout_ms": 2000}
  -> testid=placeOrder is disabled after 12ms — @e1 Place order (button, disabled)
- app_wait_for {"condition": "text", "exact": true, "target": "testid=orderNumber", "text": "Order MS-000001 placed", "timeout_ms": 15000}
  -> testid=orderNumber says exactly "Order MS-000001 placed" after 4.806s
- app_tap {"target": "label=Orders"}
  -> tapped label=Orders at (907, 2232)
- app_wait_for {"condition": "text", "exact": true, "target": "testid=orderCount", "text": "1 order"}
  -> testid=orderCount says exactly "1 order" after 8ms

## trace: checkout.test.json › WELCOME10 is spent once an order uses it
- app_terminate {"app": "dev.mobium.shop"}
  -> terminated dev.mobium.shop
- app_launch {"app": "dev.mobium.shop"}
  -> launched dev.mobium.shop
- app_dialogs {"press": "Open", "when": "Morpho Market"}
  -> 1 dialog rule(s) when "Morpho Market": press "Open" (answered 0)
- app_open_url {"url": "mobiumshop://reset"}
  -> opened mobiumshop://reset
- app_wait_for {"target": "testid=catalogList", "timeout_ms": 3000}
  -> testid=catalogList is visible after 18ms — @e9 catalogList (list)
- app_tap {"target": "testid=product_mug"}
  -> tapped testid=product_mug at (802, 1958)
- app_tap {"target": "testid=addToCart"}
  -> tapped testid=addToCart at (540, 1380)
- app_tap {"target": "testid=viewCart"}
  -> tapped testid=viewCart at (897, 2012)
- app_fill {"target": "testid=codeField", "text": "(9 characters, not recorded)"}
  -> typed "WELCOME10" into testid=codeField
- app_tap {"target": "testid=applyCode"}
  -> tapped testid=applyCode at (928, 685)
- app_tap {"target": "testid=checkoutBtn"}
  -> tapped testid=checkoutBtn at (540, 1496)
- app_tap {"target": "testid=ship_pickup"}
  -> tapped testid=ship_pickup at (540, 747)
- app_tap {"target": "testid=continueDelivery"}
  -> tapped testid=continueDelivery at (540, 1306)
- app_fill {"target": "testid=field_name", "text": "(12 characters, not recorded)"}
  -> typed "Ada Lovelace" into testid=field_name
- app_fill {"target": "testid=field_email", "text": "(15 characters, not recorded)"}
  -> typed "ada@example.com" into testid=field_email
- app_keyboard {"key": "enter"}
  -> pressed enter; focus is on backBtn, holding (empty); the keyboard is hidden
- app_tap {"target": "testid=continueBtn"}
  -> tapped testid=continueBtn at (540, 914)
- app_fill {"target": "testid=field_cardNumber", "text": "(19 characters, not recorded)"}
  -> typed "4242 4242 4242 4242" into testid=field_cardNumber
- app_fill {"target": "testid=field_cardExpiry", "text": "(5 characters, not recorded)"}
  -> typed "12/30" into testid=field_cardExpiry
- app_fill {"target": "testid=field_cardCvc", "text": "(3 characters, not recorded)"}
  -> typed 3 characters into testid=field_cardCvc, a password field — not echoed
- app_fill {"target": "testid=field_cardName", "text": "(12 characters, not recorded)"}
  -> typed "Ada Lovelace" into testid=field_cardName
- app_tap {"target": "testid=continuePayment"}
  -> tapped testid=continuePayment at (540, 1229)
- app_tap {"target": "testid=placeOrder"}
  -> tapped testid=placeOrder at (540, 1198)
- app_tap {"target": "testid=keepShopping"}
  -> tapped testid=keepShopping at (540, 1064)
- app_tap {"target": "testid=product_hat"}
  -> tapped testid=product_hat at (278, 1497)
- app_tap {"target": "testid=addToCart"}
  -> tapped testid=addToCart at (540, 1380)
- app_tap {"target": "testid=viewCart"}
  -> tapped testid=viewCart at (897, 2012)
- app_fill {"target": "testid=codeField", "text": "(9 characters, not recorded)"}
  -> typed "WELCOME10" into testid=codeField
- app_tap {"target": "testid=applyCode"}
  -> tapped testid=applyCode at (928, 685)
- app_wait_for {"condition": "text", "exact": true, "target": "testid=codeMessage", "text": "That code has already been used."}
  -> testid=codeMessage says exactly "That code has already been used." after 496ms

## trace: shop.test.json › 10% of $37.45 rounds half up to $3.75
- app_terminate {"app": "dev.mobium.shop"}
  -> terminated dev.mobium.shop
- app_launch {"app": "dev.mobium.shop"}
  -> launched dev.mobium.shop
- app_dialogs {"press": "Open", "when": "Morpho Market"}
  -> 1 dialog rule(s) when "Morpho Market": press "Open" (answered 0)
- app_open_url {"url": "mobiumshop://reset"}
  -> opened mobiumshop://reset
- app_wait_for {"target": "testid=catalogList", "timeout_ms": 3000}
  -> testid=catalogList is visible after 16ms — @e9 catalogList (list)
- app_tap {"target": "testid=product_stickers"}
  -> tapped testid=product_stickers at (802, 1569)
- app_tap {"target": "testid=qtyPlus"}
  -> tapped testid=qtyPlus at (558, 1222)
- app_tap {"target": "testid=qtyPlus"}
  -> tapped testid=qtyPlus at (558, 1222)
- app_tap {"target": "testid=qtyPlus"}
  -> tapped testid=qtyPlus at (558, 1222)
- app_tap {"target": "testid=qtyPlus"}
  -> tapped testid=qtyPlus at (558, 1222)
- app_tap {"target": "testid=addToCart"}
  -> tapped testid=addToCart at (540, 1380)
- app_tap {"target": "testid=viewCart"}
  -> tapped testid=viewCart at (897, 2012)
- app_wait_for {"condition": "text", "exact": true, "target": "testid=sumMerch", "text": "$37.45"}
  -> testid=sumMerch says exactly "$37.45" after 10ms
- app_fill {"target": "testid=codeField", "text": "(9 characters, not recorded)"}
  -> typed "WELCOME10" into testid=codeField
- app_tap {"target": "testid=applyCode"}
  -> tapped testid=applyCode at (928, 738)
- app_wait_for {"condition": "text", "exact": true, "target": "testid=sumDiscount", "text": "-$3.75"}
  -> testid=sumDiscount says exactly "-$3.75" after 18ms

## trace: shop.test.json › a category narrows the catalog
- app_terminate {"app": "dev.mobium.shop"}
  -> terminated dev.mobium.shop
- app_launch {"app": "dev.mobium.shop"}
  -> launched dev.mobium.shop
- app_dialogs {"press": "Open", "when": "Morpho Market"}
  -> 1 dialog rule(s) when "Morpho Market": press "Open" (answered 0)
- app_open_url {"url": "mobiumshop://reset"}
  -> opened mobiumshop://reset
- app_wait_for {"target": "testid=catalogList", "timeout_ms": 3000}
  -> testid=catalogList is visible after 17ms — @e9 catalogList (list)
- app_tap {"target": "testid=category_drinkware"}
  -> tapped testid=category_drinkware at (537, 536)
- app_wait_for {"condition": "text", "exact": true, "target": "testid=resultCount", "text": "2 items"}
  -> testid=resultCount says exactly "2 items" after 11ms

## trace: shop.test.json › a code applies once
- app_terminate {"app": "dev.mobium.shop"}
  -> terminated dev.mobium.shop
- app_launch {"app": "dev.mobium.shop"}
  -> launched dev.mobium.shop
- app_dialogs {"press": "Open", "when": "Morpho Market"}
  -> 1 dialog rule(s) when "Morpho Market": press "Open" (answered 0)
- app_open_url {"url": "mobiumshop://reset"}
  -> opened mobiumshop://reset
- app_wait_for {"target": "testid=catalogList", "timeout_ms": 3000}
  -> testid=catalogList is visible after 16ms — @e9 catalogList (list)
- app_tap {"target": "testid=product_hat"}
  -> tapped testid=product_hat at (278, 1497)
- app_tap {"target": "testid=addToCart"}
  -> tapped testid=addToCart at (540, 1380)
- app_tap {"target": "testid=viewCart"}
  -> tapped testid=viewCart at (897, 2012)
- app_fill {"target": "testid=codeField", "text": "(9 characters, not recorded)"}
  -> typed "WELCOME10" into testid=codeField
- app_tap {"target": "testid=applyCode"}
  -> tapped testid=applyCode at (928, 685)
- app_tap {"target": "testid=applyCode"}
  -> tapped testid=applyCode at (928, 685)
- app_wait_for {"condition": "text", "exact": true, "target": "testid=codeMessage", "text": "WELCOME10 is already applied.", "timeout_ms": 3000}
  -> testid=codeMessage says exactly "WELCOME10 is already applied." after 14ms
- app_wait_for {"condition": "text", "exact": true, "target": "testid=sumDiscount", "text": "-$2.60"}
  -> testid=sumDiscount says exactly "-$2.60" after 14ms

## trace: shop.test.json › a gift card needs an email, and takes no code
- app_terminate {"app": "dev.mobium.shop"}
  -> terminated dev.mobium.shop
- app_launch {"app": "dev.mobium.shop"}
  -> launched dev.mobium.shop
- app_dialogs {"press": "Open", "when": "Morpho Market"}
  -> 1 dialog rule(s) when "Morpho Market": press "Open" (answered 0)
- app_open_url {"url": "mobiumshop://reset"}
  -> opened mobiumshop://reset
- app_wait_for {"target": "testid=catalogList", "timeout_ms": 3000}
  -> testid=catalogList is visible after 18ms — @e9 catalogList (list)
- app_tap {"target": "testid=product_giftcard"}
  -> tapped testid=product_giftcard at (278, 2020)
- app_tap {"target": "testid=amount_25"}
  -> tapped testid=amount_25 at (115, 1306)
- app_tap {"target": "testid=addToCart"}
  -> tapped testid=addToCart at (540, 1823)
- app_wait_for {"condition": "text", "exact": true, "target": "testid=giftEmailError", "text": "Enter a valid email address."}
  -> testid=giftEmailError says exactly "Enter a valid email address." after 11ms — @e1 ScrollView (list)
- app_fill {"target": "testid=giftEmail", "text": "(18 characters, not recorded)"}
  -> typed "friend@example.com" into testid=giftEmail
- app_keyboard {"key": "enter"}
  -> pressed enter; focus is on backBtn, holding (empty); the keyboard is hidden
- app_tap {"target": "testid=addToCart"}
  -> tapped testid=addToCart at (540, 1823)
- app_tap {"target": "testid=viewCart"}
  -> tapped testid=viewCart at (897, 2012)
- app_wait_for {"condition": "text", "exact": true, "target": "testid=sumGift", "text": "$25.00"}
  -> testid=sumGift says exactly "$25.00" after 14ms
- app_wait_for {"condition": "hidden", "target": "testid=sumShipping", "timeout_ms": 2000}
  -> testid=sumShipping is hidden after 32ms
- app_fill {"target": "testid=codeField", "text": "(9 characters, not recorded)"}
  -> typed "WELCOME10" into testid=codeField
- app_tap {"target": "testid=applyCode"}
  -> tapped testid=applyCode at (928, 685)
- app_wait_for {"condition": "text", "exact": true, "target": "testid=codeMessage", "text": "Codes don't apply to gift cards."}
  -> testid=codeMessage says exactly "Codes don't apply to gift cards." after 11ms

## trace: shop.test.json › an XXL tee costs $2 more
- app_terminate {"app": "dev.mobium.shop"}
  -> terminated dev.mobium.shop
- app_launch {"app": "dev.mobium.shop"}
  -> launched dev.mobium.shop
- app_dialogs {"press": "Open", "when": "Morpho Market"}
  -> 1 dialog rule(s) when "Morpho Market": press "Open" (answered 0)
- app_open_url {"url": "mobiumshop://reset"}
  -> opened mobiumshop://reset
- app_wait_for {"target": "testid=catalogList", "timeout_ms": 3000}
  -> testid=catalogList is visible after 15ms — @e9 catalogList (list)
- app_tap {"target": "testid=product_tee"}
  -> tapped testid=product_tee at (278, 975)
- app_wait_for {"condition": "disabled", "target": "testid=addToCart"}
  -> testid=addToCart is disabled after 18ms — @e9 Add to cart (button, disabled)
- app_tap {"target": "testid=size_XXL"}
  -> tapped testid=size_XXL at (859, 1306)
- app_wait_for {"condition": "text", "exact": true, "target": "testid=productPrice", "text": "$26.00"}
  -> testid=productPrice says exactly "$26.00" after 14ms
- app_wait_for {"condition": "enabled", "target": "testid=addToCart"}
  -> testid=addToCart is enabled after 17ms — @e9 Add to cart (button)

## trace: shop.test.json › codes refused, each saying why
- app_terminate {"app": "dev.mobium.shop"}
  -> terminated dev.mobium.shop
- app_launch {"app": "dev.mobium.shop"}
  -> launched dev.mobium.shop
- app_dialogs {"press": "Open", "when": "Morpho Market"}
  -> 1 dialog rule(s) when "Morpho Market": press "Open" (answered 0)
- app_open_url {"url": "mobiumshop://reset"}
  -> opened mobiumshop://reset
- app_wait_for {"target": "testid=catalogList", "timeout_ms": 3000}
  -> testid=catalogList is visible after 13ms — @e9 catalogList (list)
- app_tap {"target": "testid=product_pins"}
  -> tapped testid=product_pins at (802, 1978)
- app_tap {"target": "testid=qtyPlus"}
  -> tapped testid=qtyPlus at (558, 1222)
- app_tap {"target": "testid=addToCart"}
  -> tapped testid=addToCart at (540, 1380)
- app_tap {"target": "testid=viewCart"}
  -> tapped testid=viewCart at (897, 2012)
- app_fill {"target": "testid=codeField", "text": "(7 characters, not recorded)"}
  -> typed "MOBIUM5" into testid=codeField
- app_tap {"target": "testid=applyCode"}
  -> tapped testid=applyCode at (928, 685)
- app_wait_for {"condition": "text", "exact": true, "target": "testid=codeMessage", "text": "Add $6.00 more to use this code."}
  -> testid=codeMessage says exactly "Add $6.00 more to use this code." after 11ms
- app_fill {"target": "testid=codeField", "text": "(9 characters, not recorded)"}
  -> typed "EXPIRED20" into testid=codeField
- app_tap {"target": "testid=applyCode"}
  -> tapped testid=applyCode at (928, 685)
- app_wait_for {"condition": "text", "exact": true, "target": "testid=codeMessage", "text": "That code has expired.", "timeout_ms": 3000}
  -> testid=codeMessage says exactly "That code has expired." after 11ms
- app_wait_for {"condition": "hidden", "target": "testid=sumDiscount", "timeout_ms": 2000}
  -> testid=sumDiscount is hidden after 37ms
- app_fill {"target": "testid=codeField", "text": "(9 characters, not recorded)"}
  -> typed "FREESTUFF" into testid=codeField
- app_tap {"target": "testid=applyCode"}
  -> tapped testid=applyCode at (928, 685)
- app_wait_for {"condition": "text", "exact": true, "target": "testid=codeMessage", "text": "That code isn't valid."}
  -> testid=codeMessage says exactly "That code isn't valid." after 14ms

## trace: shop.test.json › MOBIUM5 comes off when the cart drops under $30
- app_terminate {"app": "dev.mobium.shop"}
  -> terminated dev.mobium.shop
- app_launch {"app": "dev.mobium.shop"}
  -> launched dev.mobium.shop
- app_dialogs {"press": "Open", "when": "Morpho Market"}
  -> 1 dialog rule(s) when "Morpho Market": press "Open" (answered 0)
- app_open_url {"url": "mobiumshop://reset"}
  -> opened mobiumshop://reset
- app_wait_for {"target": "testid=catalogList", "timeout_ms": 3000}
  -> testid=catalogList is visible after 14ms — @e9 catalogList (list)
- app_tap {"target": "testid=product_hat"}
  -> tapped testid=product_hat at (278, 1497)
- app_tap {"target": "testid=addToCart"}
  -> tapped testid=addToCart at (540, 1380)
- app_tap {"target": "testid=backBtn"}
  -> tapped testid=backBtn at (75, 221)
- app_tap {"target": "testid=product_magnet"}
  -> tapped testid=product_magnet at (278, 1672)
- app_tap {"target": "testid=addToCart"}
  -> tapped testid=addToCart at (540, 1380)
- app_tap {"target": "testid=viewCart"}
  -> tapped testid=viewCart at (897, 2012)
- app_wait_for {"condition": "text", "exact": true, "target": "testid=sumMerch", "text": "$31.99"}
  -> testid=sumMerch says exactly "$31.99" after 18ms
- app_fill {"target": "testid=codeField", "text": "(7 characters, not recorded)"}
  -> typed "MOBIUM5" into testid=codeField
- app_tap {"target": "testid=applyCode"}
  -> tapped testid=applyCode at (928, 992)
- app_wait_for {"condition": "text", "exact": true, "target": "testid=sumDiscount", "text": "-$5.00"}
  -> testid=sumDiscount says exactly "-$5.00" after 15ms
- app_tap {"target": "testid=lineMinus_magnet"}
  -> tapped testid=lineMinus_magnet at (711, 739)
- app_alert {"button": "Remove"}
  -> pressed "Remove" on the dialog "Remove Works On My Emulator Magnet?"
- app_wait_for {"condition": "text", "exact": true, "target": "testid=codeMessage", "text": "Add $4.00 more to use this code."}
  -> testid=codeMessage says exactly "Add $4.00 more to use this code." after 11ms
- app_wait_for {"condition": "hidden", "target": "testid=sumDiscount"}
  -> testid=sumDiscount is hidden after 32ms

## trace: shop.test.json › out of stock cannot be added
- app_terminate {"app": "dev.mobium.shop"}
  -> terminated dev.mobium.shop
- app_launch {"app": "dev.mobium.shop"}
  -> launched dev.mobium.shop
- app_dialogs {"press": "Open", "when": "Morpho Market"}
  -> 1 dialog rule(s) when "Morpho Market": press "Open" (answered 0)
- app_open_url {"url": "mobiumshop://reset"}
  -> opened mobiumshop://reset
- app_wait_for {"target": "testid=catalogList", "timeout_ms": 3000}
  -> testid=catalogList is visible after 422ms — @e9 catalogList (list)
- app_tap {"target": "testid=product_beanie"}
  -> tapped testid=product_beanie at (802, 1518)
- app_wait_for {"target": "testid=productStock"}
  -> testid=productStock is visible after 12ms
- app_wait_for {"condition": "disabled", "target": "testid=addToCart", "timeout_ms": 2000}
  -> testid=addToCart is disabled after 9ms — @e3 Add to cart (button, disabled)
- app_tap {"target": "testid=backBtn"}
  -> tapped testid=backBtn at (75, 221)
- app_tap {"target": "testid=product_hoodie"}
  -> tapped testid=product_hoodie at (802, 1002)
- app_tap {"target": "testid=size_XL"}
  -> tapped testid=size_XL at (547, 1306)
- app_wait_for {"condition": "text", "exact": true, "target": "testid=variantStock", "text": "Out of stock in XL"}
  -> testid=variantStock says exactly "Out of stock in XL" after 18ms
- app_wait_for {"condition": "disabled", "target": "testid=addToCart", "timeout_ms": 2000}
  -> testid=addToCart is disabled after 15ms — @e7 Add to cart (button, disabled)

## trace: shop.test.json › price, low to high, starts with the magnet
- app_terminate {"app": "dev.mobium.shop"}
  -> terminated dev.mobium.shop
- app_launch {"app": "dev.mobium.shop"}
  -> launched dev.mobium.shop
- app_dialogs {"press": "Open", "when": "Morpho Market"}
  -> 1 dialog rule(s) when "Morpho Market": press "Open" (answered 0)
- app_open_url {"url": "mobiumshop://reset"}
  -> opened mobiumshop://reset
- app_wait_for {"target": "testid=catalogList", "timeout_ms": 3000}
  -> testid=catalogList is visible after 18ms — @e9 catalogList (list)
- app_tap {"target": "testid=sortMenu"}
  -> tapped testid=sortMenu at (899, 662)
- app_tap {"target": "testid=sort_price_asc"}
  -> tapped testid=sort_price_asc at (875, 935)
- app_wait_for {"target": "testid=price_magnet", "timeout_ms": 3000}
  -> testid=price_magnet is visible after 13ms — @e10 Works On My Emulator Magnet $5.99 (button)
- app_wait_for {"target": "testid=price_stickers", "timeout_ms": 3000}
  -> testid=price_stickers is visible after 15ms — @e11 CHALLENGES Sticker Pack $7.49 (button)
- app_wait_for {"condition": "hidden", "target": "testid=price_hoodie", "timeout_ms": 3000}
  -> testid=price_hoodie is hidden after 37ms

## trace: shop.test.json › removing the last line asks first, and the badge goes
- app_terminate {"app": "dev.mobium.shop"}
  -> terminated dev.mobium.shop
- app_launch {"app": "dev.mobium.shop"}
  -> launched dev.mobium.shop
- app_dialogs {"press": "Open", "when": "Morpho Market"}
  -> 1 dialog rule(s) when "Morpho Market": press "Open" (answered 0)
- app_open_url {"url": "mobiumshop://reset"}
  -> opened mobiumshop://reset
- app_wait_for {"target": "testid=catalogList", "timeout_ms": 3000}
  -> testid=catalogList is visible after 13ms — @e9 catalogList (list)
- app_tap {"target": "testid=product_mug"}
  -> tapped testid=product_mug at (802, 1958)
- app_tap {"target": "testid=addToCart"}
  -> tapped testid=addToCart at (540, 1380)
- app_tap {"target": "testid=viewCart"}
  -> tapped testid=viewCart at (897, 2012)
- app_wait_for {"target": "label=\"Cart, 1 item\""}
  -> label="Cart, 1 item" is visible after 11ms
- app_tap {"target": "testid=lineMinus_mug"}
  -> tapped testid=lineMinus_mug at (711, 458)
- app_alert {"button": "Cancel"}
  -> pressed "Cancel" on the dialog "Remove Wait For It Mug?"
- app_wait_for {"condition": "text", "exact": true, "target": "testid=lineQty_mug", "text": "1"}
  -> testid=lineQty_mug says exactly "1" after 10ms
- app_tap {"target": "testid=lineMinus_mug"}
  -> tapped testid=lineMinus_mug at (711, 458)
- app_alert {"button": "Remove"}
  -> pressed "Remove" on the dialog "Remove Wait For It Mug?"
- app_wait_for {"target": "testid=emptyCart"}
  -> testid=emptyCart is visible after 8ms
- app_wait_for {"target": "label=\"Cart, 0 items\"", "timeout_ms": 2000}
  -> label="Cart, 0 items" is visible after 9ms
- app_wait_for {"condition": "disabled", "target": "testid=checkoutBtn"}
  -> testid=checkoutBtn is disabled after 10ms — @e2 Checkout (button, disabled)

## trace: shop.test.json › search narrows the catalog
- app_terminate {"app": "dev.mobium.shop"}
  -> terminated dev.mobium.shop
- app_launch {"app": "dev.mobium.shop"}
  -> launched dev.mobium.shop
- app_dialogs {"press": "Open", "when": "Morpho Market"}
  -> 1 dialog rule(s) when "Morpho Market": press "Open" (answered 0)
- app_open_url {"url": "mobiumshop://reset"}
  -> opened mobiumshop://reset
- app_wait_for {"target": "testid=catalogList", "timeout_ms": 3000}
  -> testid=catalogList is visible after 16ms — @e9 catalogList (list)
- app_fill {"target": "testid=searchField", "text": "(3 characters, not recorded)"}
  -> typed "mug" into testid=searchField
- app_wait_for {"condition": "text", "exact": true, "target": "testid=resultCount", "text": "1 item"}
  -> testid=resultCount says exactly "1 item" after 16ms
- app_wait_for {"target": "testid=product_mug"}
  -> testid=product_mug is visible after 18ms — @e9 Wait For It Mug $16.00 (button)

## trace: shop.test.json › the catalog lists every product
- app_terminate {"app": "dev.mobium.shop"}
  -> terminated dev.mobium.shop
- app_launch {"app": "dev.mobium.shop"}
  -> launched dev.mobium.shop
- app_dialogs {"press": "Open", "when": "Morpho Market"}
  -> 1 dialog rule(s) when "Morpho Market": press "Open" (answered 0)
- app_open_url {"url": "mobiumshop://reset"}
  -> opened mobiumshop://reset
- app_wait_for {"target": "testid=catalogList", "timeout_ms": 3000}
  -> testid=catalogList is visible after 13ms — @e9 catalogList (list)
- app_wait_for {"condition": "text", "exact": true, "target": "testid=resultCount", "text": "13 items"}
  -> testid=resultCount says exactly "13 items" after 12ms
- app_wait_for {"condition": "text", "exact": true, "target": "testid=price_tee", "text": "$24.00"}
  -> testid=price_tee says exactly "$24.00" after 15ms — @e10 Logo Tee $24.00 (button)

## trace: shop.test.json › the quantity stops at 10
- app_terminate {"app": "dev.mobium.shop"}
  -> terminated dev.mobium.shop
- app_launch {"app": "dev.mobium.shop"}
  -> launched dev.mobium.shop
- app_dialogs {"press": "Open", "when": "Morpho Market"}
  -> 1 dialog rule(s) when "Morpho Market": press "Open" (answered 0)
- app_open_url {"url": "mobiumshop://reset"}
  -> opened mobiumshop://reset
- app_wait_for {"target": "testid=catalogList", "timeout_ms": 3000}
  -> testid=catalogList is visible after 17ms — @e9 catalogList (list)
- app_tap {"target": "testid=product_mug"}
  -> tapped testid=product_mug at (802, 1958)
- app_tap {"target": "testid=qtyPlus"}
  -> tapped testid=qtyPlus at (558, 1222)
- app_tap {"target": "testid=qtyPlus"}
  -> tapped testid=qtyPlus at (558, 1222)
- app_tap {"target": "testid=qtyPlus"}
  -> tapped testid=qtyPlus at (558, 1222)
- app_tap {"target": "testid=qtyPlus"}
  -> tapped testid=qtyPlus at (558, 1222)
- app_tap {"target": "testid=qtyPlus"}
  -> tapped testid=qtyPlus at (558, 1222)
- app_tap {"target": "testid=qtyPlus"}
  -> tapped testid=qtyPlus at (558, 1222)
- app_tap {"target": "testid=qtyPlus"}
  -> tapped testid=qtyPlus at (558, 1222)
- app_tap {"target": "testid=qtyPlus"}
  -> tapped testid=qtyPlus at (558, 1222)
- app_tap {"target": "testid=qtyPlus"}
  -> tapped testid=qtyPlus at (558, 1222)
- app_wait_for {"condition": "text", "exact": true, "target": "testid=qtyValue", "text": "10"}
  -> testid=qtyValue says exactly "10" after 9ms
- app_wait_for {"condition": "disabled", "target": "testid=qtyPlus", "timeout_ms": 2000}
  -> testid=qtyPlus is disabled after 8ms — @e2 + (button, disabled)

## trace: shop.test.json › two tees and a mug, with WELCOME10
- app_terminate {"app": "dev.mobium.shop"}
  -> terminated dev.mobium.shop
- app_launch {"app": "dev.mobium.shop"}
  -> launched dev.mobium.shop
- app_dialogs {"press": "Open", "when": "Morpho Market"}
  -> 1 dialog rule(s) when "Morpho Market": press "Open" (answered 0)
- app_open_url {"url": "mobiumshop://reset"}
  -> opened mobiumshop://reset
- app_wait_for {"target": "testid=catalogList", "timeout_ms": 3000}
  -> testid=catalogList is visible after 13ms — @e9 catalogList (list)
- app_tap {"target": "testid=product_tee"}
  -> tapped testid=product_tee at (278, 975)
- app_tap {"target": "testid=size_M"}
  -> tapped testid=size_M at (404, 1306)
- app_tap {"target": "testid=qtyPlus"}
  -> tapped testid=qtyPlus at (558, 1465)
- app_tap {"target": "testid=addToCart"}
  -> tapped testid=addToCart at (540, 1623)
- app_wait_for {"target": "testid=addedNotice"}
  -> testid=addedNotice is visible after 13ms
- app_wait_for {"target": "label=\"Cart, 2 items\""}
  -> label="Cart, 2 items" is visible after 16ms — @e11 Cart, 2 items Cart (button)
- app_tap {"target": "testid=backBtn"}
  -> tapped testid=backBtn at (75, 221)
- app_tap {"target": "testid=product_mug"}
  -> tapped testid=product_mug at (802, 1958)
- app_tap {"target": "testid=addToCart"}
  -> tapped testid=addToCart at (540, 1380)
- app_tap {"target": "testid=viewCart"}
  -> tapped testid=viewCart at (897, 2012)
- app_wait_for {"condition": "text", "exact": true, "target": "testid=sumMerch", "text": "$64.00"}
  -> testid=sumMerch says exactly "$64.00" after 18ms
- app_fill {"target": "testid=codeField", "text": "(9 characters, not recorded)"}
  -> typed "welcome10" into testid=codeField
- app_tap {"target": "testid=applyCode"}
  -> tapped testid=applyCode at (928, 939)
- app_wait_for {"condition": "text", "exact": true, "target": "testid=codeMessage", "text": "WELCOME10 applied: 10% off merchandise."}
  -> testid=codeMessage says exactly "WELCOME10 applied: 10% off merchandise." after 15ms
- app_wait_for {"condition": "text", "exact": true, "target": "testid=sumDiscount", "text": "-$6.40"}
  -> testid=sumDiscount says exactly "-$6.40" after 13ms
- app_wait_for {"condition": "text", "exact": true, "target": "testid=sumTotal", "text": "$57.60"}
  -> testid=sumTotal says exactly "$57.60" after 16ms



# The test format

A test file is JSON:

    {
      "app": "<package>",            // stopped and launched fresh before every test
      "beforeEach": [<step>...],     // optional: run before each test's own steps
      "tests": [
        {"name": "...", "description": "...", "steps": [<step>...],
         "each": [{"key": "value", ...}, ...]}   // optional, see below
      ]
    }

A step is one tool call, in the long form
`{"name": "app_tap", "arguments": {"target": "text=Network & internet"}}`, or
the shorthand: one key, the tool's name without `app_`, whose value is its
arguments or, as a string, its main argument — `{"tap": "text=Network &
internet"}`, `{"fill": {"target": "testid=search", "text": "wifi"}}`.

An assertion is an `app_wait_for` step —
`{"wait_for": {"target": "text=Internet", "condition": "visible"}}` — or an
expect, which reads a read-only tool until a field of its structured answer
equals a value:

    {"expect": {"tool": "app_state", "arguments": {"app": "com.android.settings"},
                "field": "state", "equals": "foreground", "not": false, "timeout_ms": 5000}}

`"soft": true` beside a step records an assertion's failure and goes on.

`each` runs a test once per case. `${key}` in any string of its steps (and in
its name) is that case's value:

    {"name": "search finds ${what}",
     "each": [{"what": "wifi"}, {"what": "bluetooth"}],
     "steps": [{"fill": {"target": "testid=search", "text": "${what}"}},
               {"wait_for": {"target": "text=${what}", "condition": "visible"}}]}

A test with `each` and no `${key}` in its name has its cases numbered.

