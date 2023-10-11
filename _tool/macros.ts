// deno run _tool/macros.ts | pbcopy

const makeEiji = (p: {code: string }) => `
eiji_${p.code}: eiji_${p.code} {
    label = "eiji_${p.code}";
    compatible = "zmk,behavior-macro";
    #binding-cells = <0>;
    bindings
        = <&kp EIJI>
        , <&macro_press &kp LS(${p.code.toUpperCase()})>
        , <&macro_pause_for_release>
        , <&macro_release &kp LS(${p.code.toUpperCase()})>
        ;
};
`

const makeNum = (p: {code: number }) => `
my_num_${p.code}: my_num_${p.code} {
    label = "my_num_${p.code}";
    compatible = "zmk,behavior-macro";
    #binding-cells = <0>;
    bindings
        = <&kp EIJI>
        , <&macro_press &kp N${p.code}>
        , <&macro_pause_for_release>
        , <&macro_release &kp N${p.code}>
        ;
};
`

// _|&!?
// UNDERSCORE
// PIPE
// AMPERSAND
// EXCLAMATION
// QUESTION

// #,.;:@
// HASH
// COMMA
// PERIOD
// SEMICOLON
// COLON
// AT_SIGN

// "'`/\
// DOUBLE_QUOTES
// SINGLE_QUOTE
// GRAVE
// SLASH
// BACKSLASH


const makeSymbol1 = (p: {code: string }) => `
my_${p.code}: my_${p.code} {
    label = "my_${p.code}";
    compatible = "zmk,behavior-macro";
    #binding-cells = <0>;
    bindings
        = <&kp EIJI>
        , <&macro_press &kp ${p.code}>
        , <&macro_pause_for_release>
        , <&macro_release &kp ${p.code}>
        ;
};
`

// ^<>[]
// CARET
// LESS_THAN
// GREATER_THAN
// LEFT_BRACKET
// RIGHT_BRACKET

// =+-*%$
// EQUAL
// PLUS
// MINUS
// ASTERISK
// PERCENT
// DOLLAR

// ~(){}
// TILDE
// LEFT_PARENTHESIS
// RIGHT_PARENTHESIS
// LEFT_BRACE
// RIGHT_BRACE

const makeSymbol2 = (p: {code: string }) => `
my_${p.code}: my_${p.code} {
    label = "my_${p.code}";
    compatible = "zmk,behavior-macro";
    #binding-cells = <0>;
    bindings
        = <&kp EIJI>
        , <&macro_press &kp ${p.code}>
        , <&macro_pause_for_release>
        , <&macro_release &kp ${p.code}>
        ;
};
`

const eiji = [...Array(26)].map((_, b) => (10 + b).toString(36)).map(v => makeEiji({code: v})).join('')
const num = [...Array(10)].map((_, i) => i).map(v => makeNum({code: v})).join('')
const symbol1 = ["UNDERSCORE","PIPE","AMPERSAND","EXCLAMATION","QUESTION","HASH","COMMA","PERIOD","SEMICOLON","COLON","AT_SIGN","DOUBLE_QUOTES","SINGLE_QUOTE","GRAVE","SLASH","BACKSLASH"].map(v => makeSymbol1({code: v})).join('')
const symbol2 = ["CARET","LESS_THAN","GREATER_THAN","LEFT_BRACKET","RIGHT_BRACKET","EQUAL","PLUS","MINUS","ASTERISK","PERCENT","DOLLAR","TILDE","LEFT_PARENTHESIS","RIGHT_PARENTHESIS","LEFT_BRACE","RIGHT_BRACE",].map(v => makeSymbol2({code: v})).join('')

console.log(`${eiji}
${num}
${symbol1}
${symbol2}`)
