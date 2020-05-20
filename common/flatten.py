import pandas as pd


def flatten(array):
    """Convierte un array de habilidades en dataframe.

    Esta funcion convierte un array de tipo:

	[
		"Hola - Adios - Como - Estas",
		"Hola - Como - Estas",
		"Hola - Adios - Como",
		"Adios - Como - Estas",
		"Hola - Adios",
		"Hola",
	]

    Y regresa un dataframe de tipo:

    hab1, hab2, hab3, hab4
    1,1,1,1
    1,0,1,1
    0,1,1,1
    1,1,0,0
    1,0,0,0

    Parameters
    ----------
    array : list
        array a cambiar.

    Returns
    -------
    pandas.DataFrame
        DataFrame a regresar.

    """
    cols = {}

    for item in array:
        for x in item.split(" - "):
            cols[x] = 0

    obs = []

    for item in array:
        dt = {key: val for key, val in cols.items()}
        for x in item.split(" - "):
            dt[x] = 1
        obs.append(dt)

    df = pd.DataFrame(obs, columns=[key for key, val in cols.items()])

    return df

