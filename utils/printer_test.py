from escpos.printer import Network
from escpos.exceptions import Error
from escpos.exceptions import TextError
try:
    ticket = Network("192.168.1.100", port=9100, timeout=3) #Printer IP Address
    if ticket.is_online():
        ticket.text("Hello World\n")
        ticket.barcode('1324354657687', 'EAN13', 64, 2, '', '')
        ticket.cut()

except Error as e:
    print(f"Error: {e}")    

except TextError as e:
    print(f"Error: {e}")

finally:
    if 'ticket' in locals():
        ticket.close()
