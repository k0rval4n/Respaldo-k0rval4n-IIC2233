def menu():
    #import utils.loader
    import utils.pretty_print
    
    #item = utils.loader.cargar_items()
    seguir = True
    while seguir:
        utils.pretty_print.print_opciones_menu()
        opcion = input()
        if opcion.lower() == "a":
            pass
        elif opcion.lower() == "b":
            pass
        elif opcion.lower() == "c":
            pass
        elif opcion.lower() == "d":
            pass
        elif opcion.lower() == "e":
            utils.pretty_print.print_salida()
            seguir = False

        

menu()