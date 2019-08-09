
==================================================
Account Banking Sepa - COR1
==================================================

Este módulo permite establecer el termino COR1 en el identificador de un
mandato de adeudo para generar el fichero sepa para este tipo de gestión de remesas.

Installation
============

Para instalar este módulo, es necesario tener disponible el módulo
*account_banking_sepa_direct_debit* del repositorio
https://github.com/OCA/bank-payment

Usage
=====

Se dispone de un nuevo valor "Básico COR1" en el mandato directo, si se marca,
al exportar la órden de cobro con ese modo de pago utilizará COR1
para escribir el fichero.
