// deno run _tool/behaviors.ts | pbcopy

const makeMy = (p: {code: string }) => `
my_${p.code}: my_${p.code} {
    compatible = "zmk,behavior-mod-morph";
    label = "my_${p.code}";
    #binding-cells = <0>;
    bindings = <&kp ${p.code.toUpperCase()}>, <&eiji_${p.code}>;
    mods = <(MOD_LSFT)>;
};
`


console.log([...Array(26)].map((_, b) => (10 + b).toString(36)).map(v => makeMy({code: v})).join(''))
