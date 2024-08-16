

from microMLP import MicroMLP    # NOTA IMPORTANTE:
                                 # En la RP2040 hay que cargar
                                 # previemente en la memoria del
                                 # dispositivo para que no se
                                 # genere un error al cargar la
                                 # librería microMLP.
import machine
machine.freq(270000000)


mlp = MicroMLP.Create( neuronsByLayers           = [1, 4, 1],
                       activationFuncName        = MicroMLP.ACTFUNC_HEAVISIDE,
                       layersAutoConnectFunction = MicroMLP.LayersFullConnect )


C1 = 0
C2 = 8
C3 = 15
C4 = 22
C5 = 100
F1 = 32
F2 = 46.4
F3 = 59
F4 = 71.4
F5 = 212

Grados_C1 = MicroMLP.NNValue.FromAnalogSignal(C1)
Grados_F1 = MicroMLP.NNValue.FromAnalogSignal(F1)
Grados_C2 = MicroMLP.NNValue.FromAnalogSignal(C2)
Grados_F2 = MicroMLP.NNValue.FromAnalogSignal(F2)
Grados_C3 = MicroMLP.NNValue.FromAnalogSignal(C3)
Grados_F3 = MicroMLP.NNValue.FromAnalogSignal(F3)
Grados_C4 = MicroMLP.NNValue.FromAnalogSignal(C4)
#Ecuac4    = MicroMLP.NNValue.FromAnalogSignal((C4*1.8)+32)
Grados_F4 = MicroMLP.NNValue.FromAnalogSignal(F4)
Grados_C5 = MicroMLP.NNValue.FromAnalogSignal(C5)
Grados_F5 = MicroMLP.NNValue.FromAnalogSignal(F5)

mlp.AddExample( [Grados_C1], [Grados_F1] )
mlp.AddExample( [Grados_C2], [Grados_F2] )
mlp.AddExample( [Grados_C3], [Grados_F3] )
mlp.AddExample( [Grados_C4], [Grados_F4] )
mlp.AddExample( [Grados_C5], [Grados_F5] )



learnCount = mlp.LearnExamples()


print(mlp.Predict([Grados_C1])[0].AsFloat)
print(mlp.Predict([Grados_C2])[0].AsFloat)
print(mlp.Predict([Grados_C3])[0].AsFloat)
print(mlp.Predict([Grados_C4])[0].AsFloat)
print(mlp.Predict([Grados_C5])[0].AsFloat)
