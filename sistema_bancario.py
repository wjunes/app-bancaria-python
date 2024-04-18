import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime


 
class Cliente:
    def __init__(self, direccion):
        self.direccion = direccion
        self.cuentas = []
        
    def realizar_transaccion(self, cuenta, transaccion):
        transaccion.registrar(cuenta)
        
    def agregar_cuenta(self, cuenta):
        self.cuentas.append(cuenta)
            
class PersonaFisica(Cliente):
    def __init__(self, nombre, fecha_nacimiento, ci, direccion):
        super().__init__(direccion)
        self.nombre = nombre
        self.fecha_nacimiento = fecha_nacimiento
        self.ci = ci

class Cuenta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historial = Historial()
        
        
    @classmethod
    def nueva_cuenta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historial(self):
        return self._historial
    
    
    def retiro(self, valor):
        saldo = self.saldo
        excedio_saldo = valor > saldo
        
        if excedio_saldo:
            print("\n@@@ Operacion inválida! Su saldo es insuficiente. @@@")
            
            
        elif valor > 0:
            self._saldo -= valor
            print("\n=== Retiro realizado con éxito! ===")
            return True
        
        else:
            print("\n@@@ Operación inválida! El valor informado no es correcto. @@@")
            
            return False
        
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado con éxito! ===")
            
        else:
            print("\n @@@ Operación inválida! El valor informado no es correcto. @@@")
            return False
        
        return True
     
class CuentaCorriente(Cuenta):
    def __init__(self, numero, cliente, limite=500, limite_retiros=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_retiros = limite_retiros
        
    def retiros(self, valor):
        numero_retiros = len(
            [transaccion for transaccion in self.historial.transacciones if transaccion["tipo"] == retirar.__name__])
        
        excedio_limite = valor > self.limite
        excedio_retiros = numero_retiros >= self.limite_retiros
        
        if excedio_limite:
            print("\n@@@ Operación inválida! El valor solicitado excede el límite. @@@")
            
        elif excedio_retiros:
            print("\n @@@ Operación inválida número máximo de retiros excedido. @@@")
            
        else:
            return super().retiro(valor)
        
        return False
    
    def __str__(self):
        return f"""\
            Agencia:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nombre}
        """
            
class Historial:
    def __init__(self):
        self._transacciones = []
           
    @property
    def transacciones(self):
        return self._transacciones
    
    def agregar_transaccion(self, transaccion):
        self._transacciones.append(
            {
                "tipo": transaccion.__class__.__name__,
                "valor": transaccion.valor,
                "fecha": datetime.now().strftime('%d - %m - %y %H:%M:%s'),
            }
        )

class Transaccion(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    
    @abstractclassmethod
    def registrar(self, cuenta):
        pass

class Extraccion(Transaccion):
    def __init__(self, valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, cuenta):
        exito_transaccion = cuenta.retirar(self.valor)
        
        if exito_transaccion:
            cuenta.historial.agregar_transaccion(self)
   
class Deposito(Transaccion):

    def __init__(self, valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, cuenta):
        exito_transaccion = cuenta.depositar(self.valor)
        
        if exito_transaccion:
            cuenta.historial.agregar_transaccion(self)
      
def menu():
    menu_text = """\n
    ============== MENU ==============
    [d]\tDepositar
    [r]\tRetirar
    [e]\tExtracto
    [nc]\tNueva cuenta
    [lc]\tListar cuentas
    [nu]\tNuevo usuario
    [s]\tSalir
    => """
    return input(textwrap.dedent(menu_text))   
     
    

    
    
def filtrar_cliente(ci, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.ci == ci]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_cuenta_cliente(cliente):
    if not cliente.cuentas:
        print("\n@@@ Cliente no posee cuenta! @@@")
        return
    
    # FIXME: no permite al cliente escoger la cuenta
    return cliente.cuentas[0]

def depositar(clientes):
    ci = input("informe la CI del cliente: ")
    cliente = filtrar_cliente(ci, clientes)
    
    if not cliente:
        print("\n@@@ Cliente no encontrado @@@")
        return
    
    valor = float(input("Informe el valor del depósito: "))
    transaccion = Deposito(valor)
    
    cuenta = recuperar_cuenta_cliente(cliente)
    if not cuenta:
        return
    
    cliente.realizar_transaccion(cuenta, transaccion)
    
    
def retirar(clientes):
    ci = input("Informe la CI del cliente: ")
    cliente = filtrar_cliente(ci, clientes)
    
    if not cliente:
        print("\n@@@ Cliente no encontrado! @@@")
        return
    
    valor = float(input("Informe el valor del retiro: "))
    transaccion = retirar(valor)
    
    cuenta = recuperar_cuenta_cliente(cliente)
    if not cuenta:
        return
    
    cliente.realizar_transaccion(cuenta, transaccion)
    
    
def exibir_extracto(clientes):
    ci = input("Informe la CI del cliente")
    cliente = filtrar_cliente(ci, clientes)
    
    if not cliente:
        print("\n@@@ Cliente no encontrado! @@@")
        return
    
    cuenta = recuperar_cuenta_cliente(cliente)
    if not cuenta:
        return
    
    print("\n============== EXTRACTO =============")
    transacciones = cuenta.historial.transacciones
    
    extracto = ""
    if not transacciones:
        extracto = "No se realizaron Movimientos en la cuenta."
    else:
        for transaccion in transacciones:
            extracto += f"\n{transaccion['tipo']}:\n\t${transaccion['valor']:.2f}"
            
    print(extracto)
    print(f"\nSaldo:\n\t$ {cuenta.saldo:.2f}")
    print("==============================")
    
def crear_cliente(clientes):
    ci = input("Informe la CI (solamente el numeros): ")
    cliente = filtrar_cliente(ci, clientes)
    
    if cliente:
        print("\n@@@ Ya existe cliente con esa CI! @@@")
        return
    
    nombre = input("Informe el nombre completo: ")
    fecha_nacimiento = input("Informe la fecha de nacimiento (dd - mm - aaaa): ")
    direccion = input("Informe su dirección (calle, nro - barrio - ciudad - departamento): ")
    
    cliente = PersonaFisica(nombre=nombre, fecha_nacimiento=fecha_nacimiento, ci=ci, direccion=direccion)
    
    clientes.append(cliente)
    
    print("\n=== Cliente creado con éxito! ===")
    
     
def crear_cuenta(numero_cuenta, clientes, cuentas):
    ci = input("Informe la CI del cliente: ")
    cliente = filtrar_cliente(ci, clientes)
    
    if not cliente:
        print("\n@@@ Cliente no encontrado, flujo de creación de cuenta abortado! @@@")
        return
    
    cuenta = CuentaCorriente.nueva_cuenta(cliente=cliente, numero=numero_cuenta)
    cuentas.append(cuenta)
    cliente.cuentas.append(cuenta)
    
    print("\n=== Cuenta creada con éxito! ===")
    
def listar_cuentas(cuentas):
    for cuenta in cuentas:
        print("=" * 100)
        print(textwrap.dedent(str(cuenta)))
    
    
    
    
def main():
    clientes = []
    cuentas = []

    while True:
        
        opcion = menu()
        
        if opcion == "d":
            depositar(clientes)
            
        elif opcion == "r":
            retirar(clientes)
            
        elif opcion == "e":
            exibir_extracto(clientes)
            
        elif opcion == "nu":
            crear_cliente(clientes)
            
        elif opcion == "nc":
            numero_cuenta = len(cuentas) + 1
            crear_cuenta(numero_cuenta, clientes, cuentas)
            
        elif opcion == "lc":
            listar_cuentas(cuentas)
            
        elif opcion == "s":
            break
        
        else:
            print("\n@@@ Operación Inválida, por favor seleccione nuevamente la operación deseada. @@@")
        
main()      
