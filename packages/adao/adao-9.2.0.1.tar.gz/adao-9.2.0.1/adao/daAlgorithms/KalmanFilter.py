# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2018 EDF R&D
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
# See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#
# Author: Jean-Philippe Argaud, jean-philippe.argaud@edf.fr, EDF R&D

import logging
from daCore import BasicObjects
import numpy

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "KALMANFILTER")
        self.defineRequiredParameter(
            name     = "EstimationOf",
            default  = "State",
            typecast = str,
            message  = "Estimation d'etat ou de parametres",
            listval  = ["State", "Parameters"],
            )
        self.defineRequiredParameter(
            name     = "StoreInternalVariables",
            default  = False,
            typecast = bool,
            message  = "Stockage des variables internes ou intermédiaires du calcul",
            )
        self.defineRequiredParameter(
            name     = "StoreSupplementaryCalculations",
            default  = [],
            typecast = tuple,
            message  = "Liste de calculs supplémentaires à stocker et/ou effectuer",
            listval  = ["APosterioriCorrelations", "APosterioriCovariance", "APosterioriStandardDeviations", "APosterioriVariances", "BMA", "CurrentState", "CostFunctionJ", "CostFunctionJb", "CostFunctionJo", "Innovation"]
            )
        self.requireInputArguments(
            mandatory= ("Xb", "Y", "HO", "R", "B" ),
            optional = ("U", "EM", "CM", "Q"),
            )

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, R, B, Q)
        #
        if self._parameters["EstimationOf"] == "Parameters":
            self._parameters["StoreInternalVariables"] = True
        #
        # Opérateurs
        # ----------
        Ht = HO["Tangent"].asMatrix(Xb)
        Ha = HO["Adjoint"].asMatrix(Xb)
        #
        if self._parameters["EstimationOf"] == "State":
            Mt = EM["Tangent"].asMatrix(Xb)
            Ma = EM["Adjoint"].asMatrix(Xb)
        #
        if CM is not None and "Tangent" in CM and U is not None:
            Cm = CM["Tangent"].asMatrix(Xb)
        else:
            Cm = None
        #
        # Nombre de pas identique au nombre de pas d'observations
        # -------------------------------------------------------
        if hasattr(Y,"stepnumber"):
            duration = Y.stepnumber()
        else:
            duration = 2
        #
        # Précalcul des inversions de B et R
        # ----------------------------------
        if self._parameters["StoreInternalVariables"] \
            or "CostFunctionJ" in self._parameters["StoreSupplementaryCalculations"] \
            or "CostFunctionJb" in self._parameters["StoreSupplementaryCalculations"] \
            or "CostFunctionJo" in self._parameters["StoreSupplementaryCalculations"]:
            BI = B.getI()
            RI = R.getI()
        #
        # Initialisation
        # --------------
        Xn = Xb
        Pn = B
        #
        self.StoredVariables["Analysis"].store( Xn.A1 )
        if "APosterioriCovariance" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["APosterioriCovariance"].store( Pn.asfullmatrix(Xn.size) )
            covarianceXa = Pn
        Xa               = Xn
        previousJMinimum = numpy.finfo(float).max
        #
        for step in range(duration-1):
            if hasattr(Y,"store"):
                Ynpu = numpy.asmatrix(numpy.ravel( Y[step+1] )).T
            else:
                Ynpu = numpy.asmatrix(numpy.ravel( Y )).T
            #
            if U is not None:
                if hasattr(U,"store") and len(U)>1:
                    Un = numpy.asmatrix(numpy.ravel( U[step] )).T
                elif hasattr(U,"store") and len(U)==1:
                    Un = numpy.asmatrix(numpy.ravel( U[0] )).T
                else:
                    Un = numpy.asmatrix(numpy.ravel( U )).T
            else:
                Un = None
            #
            if self._parameters["EstimationOf"] == "State":
                Xn_predicted = Mt * Xn
                if Cm is not None and Un is not None: # Attention : si Cm est aussi dans M, doublon !
                    Cm = Cm.reshape(Xn.size,Un.size) # ADAO & check shape
                    Xn_predicted = Xn_predicted + Cm * Un
                Pn_predicted = Q + Mt * Pn * Ma
            elif self._parameters["EstimationOf"] == "Parameters":
                # --- > Par principe, M = Id, Q = 0
                Xn_predicted = Xn
                Pn_predicted = Pn
            #
            if self._parameters["EstimationOf"] == "State":
                d  = Ynpu - Ht * Xn_predicted
            elif self._parameters["EstimationOf"] == "Parameters":
                d  = Ynpu - Ht * Xn_predicted
                if Cm is not None and Un is not None: # Attention : si Cm est aussi dans H, doublon !
                    d = d - Cm * Un
            #
            _A = R + Ht * Pn_predicted * Ha
            _u = numpy.linalg.solve( _A , d )
            Xn = Xn_predicted + Pn_predicted * Ha * _u
            Kn = Pn_predicted * Ha * (R + Ht * Pn_predicted * Ha).I
            Pn = Pn_predicted - Kn * Ht * Pn_predicted
            #
            self.StoredVariables["Analysis"].store( Xn.A1 )
            if "APosterioriCovariance" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["APosterioriCovariance"].store( Pn )
            if "Innovation" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["Innovation"].store( numpy.ravel( d.A1 ) )
            if self._parameters["StoreInternalVariables"] \
                or "CurrentState" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["CurrentState"].store( Xn )
            if self._parameters["StoreInternalVariables"] \
                or "CostFunctionJ" in self._parameters["StoreSupplementaryCalculations"] \
                or "CostFunctionJb" in self._parameters["StoreSupplementaryCalculations"] \
                or "CostFunctionJo" in self._parameters["StoreSupplementaryCalculations"]:
                Jb  = 0.5 * (Xn - Xb).T * BI * (Xn - Xb)
                Jo  = 0.5 * d.T * RI * d
                J   = float( Jb ) + float( Jo )
                self.StoredVariables["CostFunctionJb"].store( Jb )
                self.StoredVariables["CostFunctionJo"].store( Jo )
                self.StoredVariables["CostFunctionJ" ].store( J )
                if J < previousJMinimum:
                    previousJMinimum  = J
                    Xa                = Xn
                    if "APosterioriCovariance" in self._parameters["StoreSupplementaryCalculations"]:
                        covarianceXa  = Pn
            else:
                Xa = Xn
            #
        #
        # Stockage supplementaire de l'optimum en estimation de parametres
        # ----------------------------------------------------------------
        if self._parameters["EstimationOf"] == "Parameters":
            self.StoredVariables["Analysis"].store( Xa.A1 )
            if "APosterioriCovariance" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["APosterioriCovariance"].store( covarianceXa )
        #
        if "BMA" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(Xa) )
        #
        self._post_run(HO)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC \n')
