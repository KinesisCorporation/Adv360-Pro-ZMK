# Things I tried
The following homerow mods are bad, the typing gets very slow and the mods are activated easily if typing gets faster.
But in order to actually use the mods, like capitalizing letters, I have to press both keys very fast, otherwise it
outputs 2 letters. Terrible.
```
lh_pht: left_positional_hold_tap {
        compatible = "zmk,behavior-hold-tap";
#binding-cells = <2>;
flavor = "tap-unless-interrupted";
tapping-term-ms = <100>;
// <---[[produces tap if held longer than tapping-term-ms]]
        quick-tap-ms = <200>;
bindings = <&kp>, <&kp>;
hold-trigger-key-positions = <7 8 9 10 11 12 13 21 22 23 24 25 26 27 39 40 41 42 43 44 45 54 55 56 57 58 59 71 72 73 74 75>;
// <---[[right-hand keys]]
      };

rh_pht: right_positional_hold_tap {
        compatible = "zmk,behavior-hold-tap";
#binding-cells = <2>;
flavor = "tap-unless-interrupted";
tapping-term-ms = <100>;
// <---[[produces tap if held longer than tapping-term-ms]]
        quick-tap-ms = <200>;
bindings = <&kp>, <&kp>;
hold-trigger-key-positions = <0 1 2 3 4 5 6 14 15 16 17 18 19 20 28 29 30 31 32 33 34 46 47 48 49 50 51 60 61 62 63 64>;
// <---[[left-hand keys]]
      };
      
...

&kp ESC   &lh_pht LSHFT A     &lh_pht LCTRL S    &lh_pht LALT D    &lh_pht LGUI F      &kp G  &kp GRAVE           &kp LGUI  &kp LALT  &kp RALT  &kp RGUI       &none &kp H  &rh_pht RGUI J  &rh_pht RALT K     &rh_pht RCTRL L    &rh_pht RSHFT SEMI &kp SQT

```