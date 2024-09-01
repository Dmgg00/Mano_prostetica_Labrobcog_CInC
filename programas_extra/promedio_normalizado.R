# Cargar las librerías
library(ggplot2)
library(dplyr)
library(zoo)

# Función para cargar y filtrar datos alrededor del pico, incluyendo un margen de ruido
load_and_filter_data <- function(filepath, window_size = 10, margin = 30) {
  # Cargar los datos
  data <- tryCatch({
    read.table(filepath, header = FALSE)
  }, error = function(e) {
    message("Error al cargar el archivo: ", filepath)
    return(NULL)
  })
  
  if (is.null(data) || ncol(data) != 1) {
    message("El archivo ", filepath, " no tiene el formato esperado.")
    return(NULL)
  }
  
  df <- data.frame(Index = 1:nrow(data), Value = data$V1)
  
  # Encontrar el pico
  peak_index <- which.max(df$Value)
  
  # Definir el intervalo alrededor del pico con margen de ruido
  start_index <- max(1, peak_index - margin)
  end_index <- min(nrow(df), peak_index + window_size + margin)
  
  # Filtrar los datos
  df_filtered <- df[start_index:end_index, ]
  
  # Ajustar el índice para que el gráfico comience en 0
  df_filtered$Aligned_Index <- df_filtered$Index - start_index
  
  # Ajustar los valores para que todos empiecen en el mismo nivel
  df_filtered$Adjusted_Value <- df_filtered$Value - df_filtered$Value[1]
  
  return(df_filtered)
}

# Directorio que contiene los archivos de datos
directory <- "C:/Users/emili/OneDrive/Escritorio/Git/Mano_prostetica_Labrobcog_CInC/Datos por modificar/datos_final/cerrar_cortados"

# Obtener una lista de todos los archivos de datos en el directorio
filepaths <- list.files(directory, full.names = TRUE)

# Cargar y filtrar los datos de todos los archivos
filtered_data_list <- lapply(filepaths, load_and_filter_data)

# Eliminar elementos NULL de la lista
filtered_data_list <- filtered_data_list[!sapply(filtered_data_list, is.null)]

# Combinar todos los data frames en uno solo, añadiendo una columna para identificar el archivo
combined_df <- do.call(rbind, lapply(seq_along(filtered_data_list), function(i) {
  df <- filtered_data_list[[i]]
  df$File <- paste("Archivo", i)
  return(df)
}))

# Calcular el promedio de los picos ajustados para cada serie
peak_values <- sapply(filtered_data_list, function(df) max(df$Adjusted_Value))
average_peak <- mean(peak_values)

# Mostrar el promedio del pico ajustado
print(paste("El promedio de los picos ajustados es:", average_peak))

# Calcular el promedio de las frecuencias ajustadas
average_df <- combined_df %>%
  group_by(Aligned_Index) %>%
  summarise(Avg_Value = mean(Adjusted_Value))

# Graficar los datos filtrados y alineados junto con la frecuencia promedio
p <- ggplot() +
  geom_line(data = combined_df, aes(x = Aligned_Index, y = Adjusted_Value, color = File, group = File), alpha = 0.5) +
  geom_line(data = average_df, aes(x = Aligned_Index, y = Avg_Value), color = "red", size = 1) +
  scale_color_discrete(guide = 'none') +  # Mantener los colores pero eliminar la leyenda
  labs(title = "Datos Filtrados y Alineados con Frecuencia Promedio",
       x = "Índice Alineado",
       y = "Valor Ajustado") +
  theme_minimal() +
  theme(plot.background = element_rect(fill = "white", color = NA))

# Mostrar el gráfico
print(p)

# Guardar el gráfico como un archivo de imagen con fondo blanco
ggsave("4.png", plot = p, bg = "white")
