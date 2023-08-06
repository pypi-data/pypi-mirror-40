import torch
import torch.distributed as dist


def broadcast(tensor, src):
    return dist.broadcast(tensor, src=src)


def elementwise_min(tensor):
    dist.all_reduce(tensor, op=dist.reduce_op.MIN)
    return tensor


def aggregate_gradients(model, world_size, average_models=False):
    """Average gradients of models across all processes."""
    # all_reduce the gradients.
    for ind, param in enumerate(model.parameters()):
        # all reduce.
        dist.all_reduce(param.grad.data, op=dist.reduce_op.SUM)

        if average_models:
            param.grad.data /= world_size


def global_average(sum, count):
    def helper(array):
        array = torch.Tensor(array)
        dist.all_reduce(array, op=dist.reduce_op.SUM)
        return array[0] / array[1]
    avg = helper([sum, count])
    return avg
