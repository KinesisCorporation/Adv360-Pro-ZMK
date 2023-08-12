// deno run _tool/fmt.ts | pbcopy

const bindings = `
&none           &none           &none           &none           &none           &none           &none                                                                                                                     &none           &none           &none           &none           &none           &none           &none
&none           &_q             &_w             &_e             &_r             &_t             &none                                                                                                                     &none           &_y             &_u             &_i             &_o             &_p             &none
&kp SPACE       &_a             &_s             &_d             &_f             &_g             &none                   &bootloader     &bt BT_CLR      &none           &none           &none           &bootloader       &none           &_h             &_j             &_k             &_l             &lt MY_SEMI     &kp BACKSPACE
&kp ESCAPE      &_z             &_x             &_c             &_v             &_b                     &none           &none           &kp LALT        &none           &none           &none           &none           &none             &_n             &_m             &_up            &lt MY_TAB      &lt MY_DEL      &kp RETURN
&none           &none           &mo L_SYM2      &mo L_SYM1      &mo L_NUM                                               &mt LL          &mt LR          &kp LCTRL       &none           &mt RL          &mt RR                                            &_left          &_down          &_right         &none           &none
`

const blockWidth = 15
const pad = 3

const [l1, l2, l3, l4, l5] = bindings.split(/\n/)
    .filter(v => v.length)
    .map(v => v.split('&')
        .map(v => v.trim())
        .filter(Boolean)
        .map(v => `&${v}`)
        .map(v => v.padEnd(blockWidth, " "))
    ).filter(Boolean)

// 7 7
const l1L = l1.slice(0, 7).join(' ').trim()
const l1R = l1.slice(7, 14).join(' ').trim()
const l1Pad = ''.padEnd(l4.slice(6, 14).join(' ').trim().length, ' ');

// 7 7
const l2L = l2.slice(0, 7).join(' ').trim()
const l2R = l2.slice(7, 14).join(' ').trim()
const l2Pad = l1Pad

// 7 6 7
const l3L = l3.slice(0, 7).join(' ').trim()
const l3M = l3.slice(7, 13).join(' ').trim()
const l3R = l3.slice(13, 20).join(' ').trim()
const l3LPad = ''.padEnd(pad + blockWidth + 1, ' ');
const l3RPad = ''.padEnd((l1L.length + l1Pad.length) - (l3L.length + pad + l3M.length) - blockWidth - 1, ' ');

// 6 8 6
const l4L = l4.slice(0, 6).join(' ').trim()
const l4M = l4.slice(6, 14).join(' ').trim()
const l4R = l4.slice(14, 20).join(' ').trim()
const l4LPad = ''.padEnd((l3L.length + pad) - l4L.length, ' ');
const l4RPad = ''.padEnd((l1L.length + l1Pad.length) - (l4L.length + l4LPad.length + l4M.length) + blockWidth + 1, ' ');

// 5 6 5
const l5L = l5.slice(0, 5).join(' ').trim()
const l5M = l5.slice(5, 11).join(' ').trim()
const l5R = l5.slice(11, 16).join(' ').trim()
const l5LPad = ''.padEnd((l3L.length + pad) - l5L.length + blockWidth + 1, ' ');
const l5RPad = ''.padEnd((l1L.length + l1Pad.length) - (l5L.length + l5LPad.length + l5M.length) + blockWidth + 1 + blockWidth + 1, ' ');

console.log(`${l1L}${l1Pad}${l1R}
${l2L}${l2Pad}${l2R}
${l3L}${l3LPad}${l3M}${l3RPad}${l3R}
${l4L}${l4LPad}${l4M}${l4RPad}${l4R}
${l5L}${l5LPad}${l5M}${l5RPad}${l5R}`);

