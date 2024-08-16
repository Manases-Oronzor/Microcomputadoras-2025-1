##################################################################
####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
##################################################################
####                                                          ####
####    EJEMPLO DE UNA COMPUERTO OR EXCLUSIVA (XOR) CON UN    ####
####    PERCEPTRON MULTICAPA.                                 ####
####                                                          ####
##################################################################
####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
##################################################################
####                                                          ####
####    Ver la Explicación de la XOR en:                      ####
####    https://www.youtube.com/watch?v=OWgAtvadHGU           ####
####    (Entrenamiento de Perceptrón Multicapa)               ####
####                                                          ####
##################################################################
####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
##################################################################

# -*- coding: utf-8 -*-

from microMLP import MicroMLP    # NOTA IMPORTANTE:
                                 # En la RP2040 hay que cargar
                                 # previemente en la memoria del
                                 # dispositivo para que no se
                                 # genere un error al cargar la
                                 # librería microMLP.
import machine
machine.freq(270000000)
                                 

################################################################
####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
################################################################
####                                                        ####
####   Asignación de los "LAYERS" (capas de la neuronas),   ####
####   la función de activación es "GAUSIANA" y el layer    ####
####   de función de autoconexión.                          ####
####                                                        ####
################################################################
####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
################################################################

mlp = MicroMLP.Create( neuronsByLayers           = [2, 2, 1],
                       activationFuncName        = MicroMLP.ACTFUNC_GAUSSIAN,
                       layersAutoConnectFunction = MicroMLP.LayersFullConnect )


#####################################
####XXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
#####################################
####                             ####
####   Definiciones de Estados   ####
####                             ####
#####################################
####XXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
#####################################

nnFalse  = MicroMLP.NNValue.FromBool(False)
nnTrue   = MicroMLP.NNValue.FromBool(True)


#######################################################################
####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
#######################################################################
####                                                               ####
####   Definiciones de las Entradas/Salidas de la "OR EXCLUSIVA"   ####
####                                                               ####
#######################################################################
####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
#######################################################################

mlp.AddExample( [nnFalse, nnFalse], [nnFalse] )
mlp.AddExample( [nnFalse, nnTrue ], [nnTrue ] )
mlp.AddExample( [nnTrue , nnTrue ], [nnFalse] )
mlp.AddExample( [nnTrue , nnFalse], [nnTrue ] )


#####################################################
####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
#####################################################
####                                             ####
####    Contador de la Función de Aprendizaje    ####
####                                             ####
#####################################################
####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
#####################################################

learnCount = mlp.LearnExamples()


###########################################################
####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
###########################################################
####                                                   ####
####   Imprime las Aproximaciones de la Red Neuronal   ####
####                                                   ####
###########################################################
####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
###########################################################

print( "LEARNED :" )
print( "  - False xor False = %s" % mlp.Predict([nnFalse, nnFalse])[0].AsBool )
print( "  - False xor True  = %s" % mlp.Predict([nnFalse, nnTrue] )[0].AsBool )
print( "  - True  xor True  = %s" % mlp.Predict([nnTrue , nnTrue] )[0].AsBool )
print( "  - True  xor False = %s" % mlp.Predict([nnTrue , nnFalse])[0].AsBool )