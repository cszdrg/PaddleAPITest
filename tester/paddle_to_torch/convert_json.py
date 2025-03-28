import json
import collections

with open("api_mapping.json", "r") as f:
    api_mapping = json.load(f)


regular_dict = collections.OrderedDict()
manual_matcher_dict = collections.OrderedDict()
paddle_multi_arg_to_torch_1_arg_dict = collections.OrderedDict()
paddle_args_grate_than_torch_dict = collections.OrderedDict()
default_value_diff_dict = collections.OrderedDict()

skip_torch_api = [
    "torch.ravel",
    "torch.Tensor.addmv",
    "torch.Tensor.addmv_",
    "torch.addmv",
    "torch.Tensor.addr",
    "torch.Tensor.addr_",
    "torch.addr",
    "torch.ger",
    "torch.Tensor.baddbmm",
    "torch.Tensor.baddbmm_",
    "torch.baddbmm",
	"torch.Tensor.bfloat16",
	"torch.Tensor.bool",
	"torch.Tensor.byte",
	"torch.Tensor.cdouble",
	"torch.Tensor.cfloat",
	"torch.Tensor.char",
	"torch.Tensor.double",
	"torch.Tensor.float",
	"torch.Tensor.half",
	"torch.Tensor.int",
	"torch.Tensor.long",
	"torch.Tensor.short",
    "torch.Tensor.clamp_",
    "torch.Tensor.histc",
    "torch.Tensor.movedim",
    "torch.Tensor.ger",
	"torch.Tensor.scatter_add",
	"torch.Tensor.scatter_reduce",
    "torch.Tensor.scatter_add_",
	"torch.Tensor.swapaxes",
	"torch.Tensor.swapdims",
	"torch.swapaxes",
	"torch.swapdims",
	"torch.transpose",
    "torch.Tensor.gather",
    "torch.Tensor.repeat",
    "torch.Tensor.transpose",
    "torch.Tensor.true_divide",
    "torch.Tensor.true_divide_",
    "torch.Tensor.random_",
    "torch.Tensor.vdot",
	"flash_attn.__version__.split",
	"torch.Tensor.new_tensor",
	"torch.asarray",
	"torch.from_numpy",
	"torch.scalar_tensor",
	"torch.tensor",
	"torch.autocast",
	"torch.cpu.amp.autocast",
	"torch.cuda.amp.autocast",
	"torch.Tensor.bernoulli",
	"torch.clamp_max",
	"torch.clamp_min",
	"torch.cat",
	"torch.conj_physical",
	"torch.cuda.manual_seed",
	"torch.cuda.manual_seed_all",
	"torch.cuda.comm.broadcast",
	"torch.distributed.rpc.remote",
	"torch.Tensor.new_empty",
	"torch.fliplr",
	"torch.flipud",
	"torch.Tensor.new_full",
	"torch.ge",
	"torch.gt",
	"torch.histc",
	"torch.linalg.inv_ex",
	"torch.cholesky_inverse",
	"torch.inverse",
	"torch.le",
	"torch.linalg.cholesky_ex",
	"torch.cholesky",
	"torch.linalg.diagonal",
	"torch.symeig",
	"torch.Tensor.symeig",
	"torch.linalg.lu_factor",
	"torch.linalg.lu_factor_ex",
	"torch.lu",
	"torch.triangular_solve",
	"torch.Tensor.triangular_solve",
	"torch.linalg.svdvals",
	"torch.svd",
	"torch.Tensor.svd",
	"torch.lt",
	"torch.movedim",
	"torch.Tensor.narrow",
	"torch.negative",
	"torch.nn.Dropout1d",
	"torch.nn.Module.register_module",
	"torch.nn.HuberLoss",
	"torch.nn.Softmax2d",
	"torch.nn.Softmin",
	"torch.alpha_dropout",
	"torch.celu",
	"torch.nn.functional.dropout1d",
	"torch.dropout",
	"torch.Tensor.hardshrink",
	"torch.max_pool1d",
	"torch.max_pool2d",
	"torch.max_pool3d",
	"torch.nn.functional.rrelu_",
	"torch.rrelu",
	"torch.nn.functional.softmin",
	"torch.softmax",
	"torch.special.softmax",
	"torch.Tensor.softmax",
	"torch.nn.parallel.DistributedDataParallel",
	"torch.nn.utils.parametrizations.spectral_norm",
	"torch.nn.utils.parametrizations.weight_norm",
	"torch.argwhere",
	"torch.norm",
	"torch.ne",
	"torch.Tensor.new_ones",
	"torch.Tensor.ormqr",
	"torch.pinverse",
	"torch.qr",
	"torch.rand_like",
	"torch.randn_like",
	"torch.range",
	"torch.relu",
	"torch.scatter_add",
	"torch.scatter_reduce",
	"torch.selu",
	"torch.set_default_tensor_type",
	"torch.autograd.set_grad_enabled",
	"torch.cuda.set_rng_state_all",
	"torch.slogdet",
	"torch.Tensor.slogdet",
	"torch.msort",
	"torch.sparse.FloatTensor",
	"torch.special.gammaln",
	"torch.special.log1p",
	"torch.special.log_softmax",
	"torch.special.multigammaln",
	"torch.special.psi",
	"torch.special.round",
	"torch.Tensor.stft",
	"torch.take_along_dim",
	"torch.testing.assert_allclose",
	"torch.testing.assert_close",
	"torch.true_divide",
	"torch.fix",
	"torch.from_dlpack",
	"torch.linalg.vander",
	"torch.Tensor.new_zeros",
	"torchvision.models.vgg11_bn",
	"torchvision.models.vgg13_bn",
	"torchvision.models.vgg16_bn",
	"torchvision.models.vgg19_bn",
    "torch.linalg.cross",
    "torch.Tensor.det",
    "torch.det",
    "torch.vdot",
    "torch.linalg.matmul",
]

skip_paddle_api = [
    "paddle.audio.functional.get_window",
    "paddle.nn.Pad1D",
    "paddle.nn.Pad2D",
    "paddle.nn.Pad3D",
    "paddle.nn.functional.smooth_l1_loss",
    "paddle.nn.functional.upsample",
    "paddle.nn.initializer.Constant"
]

for api in api_mapping:
    if len(api_mapping[api]) == 0:
        continue
    if "Matcher" not in api_mapping[api]:
        continue
    if "paddle_api" not in api_mapping[api]:
        continue
    if "args_list" not in api_mapping[api]:
        continue
    if api in skip_torch_api:
        continue
    
    paddle_api = api_mapping[api]["paddle_api"]
    
    if paddle_api in skip_paddle_api:
        continue

    if paddle_api in regular_dict:
        print(paddle_api + " double used")
    if paddle_api in manual_matcher_dict:
        print(paddle_api + " double used")
    if paddle_api in paddle_multi_arg_to_torch_1_arg_dict:
        print(paddle_api + " double used")
    if paddle_api in paddle_args_grate_than_torch_dict:
        print(paddle_api + " double used")
    if paddle_api in default_value_diff_dict:
        print(paddle_api + " double used")
    
    torch_api = api
    matcher = api_mapping[api]["Matcher"]
    is_generic_matcher = matcher == "GenericMatcher"
    min_input_args = api_mapping[api]["min_input_args"] if "min_input_args" in api_mapping[api] else 0
    args_list = api_mapping[api]["args_list"]
    kwargs_change = api_mapping[api]["kwargs_change"] if "kwargs_change" in api_mapping[api] else {}
    unsupport_args = api_mapping[api]["unsupport_args"] if "unsupport_args" in api_mapping[api] else []
    paddle_default_kwargs = api_mapping[api]["paddle_default_kwargs"] if "paddle_default_kwargs" in api_mapping[api] else []
    is_can_convert_directly = True if len(paddle_default_kwargs)==0 else False
    is_paddle_multi_arg_to_torch_1_arg = False
    
    paddle_torch_args_map = collections.OrderedDict()

    for arg in args_list:
        if arg in unsupport_args:
            continue
        if arg == "*":
            continue
        if arg in kwargs_change:
            if isinstance(kwargs_change[arg], list):
                for sub_arg in kwargs_change[arg]:
                    paddle_torch_args_map[sub_arg] = arg
                is_paddle_multi_arg_to_torch_1_arg = True
            else:
                if kwargs_change[arg] == "":
                    continue
                paddle_torch_args_map[kwargs_change[arg]] = arg
        else:
            paddle_torch_args_map[arg] = arg
    count = 0
    for default_arg in paddle_default_kwargs:
        if default_arg in paddle_torch_args_map:
            count += 1
        else:
            paddle_torch_args_map[default_arg] = ""
    if count == 0:
        is_paddle_args_grate_than_torch = True
    else:
        is_paddle_args_grate_than_torch = False
    
    item = collections.OrderedDict()
    item["torch_api"] = torch_api
    item["paddle_torch_args_map"] = paddle_torch_args_map
    item["min_input_args"] = min_input_args
    
    if is_generic_matcher:
        if is_can_convert_directly:
            if is_paddle_multi_arg_to_torch_1_arg:
                paddle_multi_arg_to_torch_1_arg_dict[paddle_api] = item
            else:
                regular_dict[paddle_api] = item
        else:
            if is_paddle_args_grate_than_torch:
                paddle_args_grate_than_torch_dict[paddle_api] = item
            else:
                item["paddle_default_kwargs"] = paddle_default_kwargs
                default_value_diff_dict[paddle_api] = item
    else:
        item["matcher"] = matcher
        manual_matcher_dict[paddle_api] = item
    
    
with open("paddle2torch_regular_dict.json", "w") as f:
    json.dump(regular_dict, f, indent=6)
with open("paddle2torch_manual_matcher_dict.json", "w") as f:
    json.dump(manual_matcher_dict, f, indent=6)
with open("paddle2torch_paddle_multi_arg_to_torch_1_arg_dict.json", "w") as f:
    json.dump(paddle_multi_arg_to_torch_1_arg_dict, f, indent=6)
with open("paddle2torch_paddle_args_grate_than_torch_dict.json", "w") as f:
    json.dump(paddle_args_grate_than_torch_dict, f, indent=6)
with open("paddle2torch_default_value_diff_dict.json", "w") as f:
    json.dump(default_value_diff_dict, f, indent=6)

with open("regular_api.yaml", "w") as f:
    f.write('apis:\n')
    for api in regular_dict:
        f.write("  -  "+api+'\n')
