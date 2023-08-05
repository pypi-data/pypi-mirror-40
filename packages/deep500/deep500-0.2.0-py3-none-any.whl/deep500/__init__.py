####################################
# General utilities
from .utils.tensor_desc import TensorDescriptor, tensor_t
tensordesc = TensorDescriptor

# Metrics and Events
from .utils.metric import TestMetric
from .utils.event import Event
from .utils.metrics import NormDifference, L1Error, L2Error, MaxError, DiffHeatmap, WallclockTime

# Device Types
from .utils.device import DeviceType, GPUDevice, CPUDevice

# ONNX Visitor
from .utils.onnx_interop.onnx_base_visitor import OnnxBaseVisitor  # throws error when op is not implemented
from .utils.onnx_interop.onnx_base_visitor import EmptyOnnxBaseVisitor  # does not throw error when op is not implemented

# ONNX Test Parser
from .utils.onnx_interop import parser
from .utils.onnx_interop.onnx_test_parser import OnnxTestParser

# ONNX Operators
from .utils import onnx_interop as ops

####################################
# Level 0: Operators
from .lv0.operators.operator_interface import CustomPythonOp, CustomCPPOp
from .lv0.operators.op_compiler import (CompilableOp, compile_custom_cppop,
                                        compile_custom_cppop_inline)

from .lv0.validation.metrics import DefaultOpMetrics
from .lv0.validation import test_op_forward, test_op_gradient


####################################
# Level 1: Network processing
from .lv1.network import Network
from .lv1.graph_executor import GraphExecutor
from .lv1.event import ExecutorEvent

from .lv1.validation import test_executor_inference, test_executor_backprop

####################################
# Level 2: Training
from .lv2.event import (TrainingEvent, OptimizerEvent, SamplerEvent, 
                        RunnerEvent, StopTraining)

from .lv2.dataset import Input, Dataset, NumpyDataset
from .lv2.sampler import Sampler, ShuffleSampler, ChoiceSampler   
from .lv2.optimizer import Optimizer, ThreeStepOptimizer, UpdateRuleOptimizer
from .lv2.summaries import TrainingStatistics

# Training events and statistics generators
import deep500.lv2.events as training_events

# Runner
from .lv2.runner import Runner, DefaultRunnerEvents

from .lv2.validation.metrics import TrainingAccuracy, TestAccuracy, DefaultTrainingMetrics, DatasetBias
from .lv2.validation import test_optimizer, test_training, test_sampler

####################################
# Level 3: Distributed Training

# MPI and related optimizers
try:
    from deep500.utils.mpi_helper import mpi_fork, mpi_end_barrier

    from .lv3.communication import CommunicationNetwork
    from .lv3.distributed_sampler import DistributedSampler, PartitionedDistributedSampler
    from .lv3.distributed_optimizer import DistributedOptimizer
except (ImportError, ModuleNotFoundError):
    pass  # Proper warnings are printed within imported modules
