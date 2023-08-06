import torch.nn


def _wrap(module, in_specs, out_specs):
    def forward(*inputs):
        assert len(in_specs) == len(inputs)

        order, star = inputs[0]._schema.order(in_specs[0])
        def resolve():
            return flatten([s if s!= "*" else star for s in out_specs])
        inputs_in = []
        inputs_in.append(inp[i].shift(order))

        for inp, spec in zip(inputs[1:], in_specs[1:]):
            input_in.append(inp.shift(resolve(spec)))

        output = module.forward(inputs_in._tensor)
        if isinstance(out, tuple):
            assert len(out_specs) == len(output)
            order = flatten([s if s!= "*" else star for s in out_specs])
            return tuple((NamedTensor(o, resolve(spec))
                          for o, spec in zip(output, out_specs)))
        else:
            return NamedTensor(output, resolve(out_specs[0]))
