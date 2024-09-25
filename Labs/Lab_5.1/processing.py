import sys

sys.path.append("../../")
import csvreader
import graphs
import calculations

import matplotlib.pyplot as plt
import numpy as np
from math import sqrt, pi

# Задание начальных параметров
ambient_temperature = 3377
measurement_error = 0.1

# Обработка данных для алюминия
aluminum_data = csvreader.readData("al-data.csv", 0)
aluminum_data[:, 1] -= ambient_temperature

# Нормализация данных
for series in range(3):
    for index in range(1, 6):
        aluminum_data[6 * series + index, 0] += aluminum_data[6 * series + index - 1, 0]
        aluminum_data[6 * series + index, 1] = aluminum_data[6 * series, 1] / aluminum_data[6 * series + index, 1]
    aluminum_data[6 * series, 1] = 1

# Вычисление среднего значения и погрешности
average_aluminum = (aluminum_data[:6, :] + aluminum_data[6:12, :] + aluminum_data[12:, :]) / 3
error_aluminum = 3 * np.sqrt((aluminum_data[:6, 1] - average_aluminum[:, 1])**2 +
                              (aluminum_data[6:12, 1] - average_aluminum[:, 1])**2 +
                              (aluminum_data[12:, 1] - average_aluminum[:, 1])**2)

# Построение графика и вывод результата
k_al, b_al, dk_al, db_al = graphs.plotlsqm(average_aluminum[:, 0], np.log(average_aluminum[:, 1]),
                                           np.ones(6) * measurement_error, error_aluminum / average_aluminum[:, 1],
                                           title="Логарифмическое ослабление потока для Al",
                                           xlabel="Толщина образца (мм)",
                                           ylabel="ln(N0 / N)",
                                           bflag=False)
print(f"μ_Al = ({k_al * 10:.5f} ± {dk_al * 10:.5f}) cm^-1")
print(f"hω_Al = 0.75 MeV")
print()

# Обработка данных для железа
iron_data = csvreader.readData("fe-data.csv", 0)
iron_data[:, 1] -= ambient_temperature

# Нормализация данных
for series in range(3):
    for index in range(1, 6):
        iron_data[6 * series + index, 0] += iron_data[6 * series + index - 1, 0]
        iron_data[6 * series + index, 1] = iron_data[6 * series, 1] / iron_data[6 * series + index, 1]
    iron_data[6 * series, 1] = 1

# Вычисление среднего значения и погрешности
average_iron = (iron_data[:6, :] + iron_data[6:12, :] + iron_data[12:, :]) / 3
error_iron = 3 * np.sqrt((iron_data[:6, 1] - average_iron[:, 1])**2 +
                          (iron_data[6:12, 1] - average_iron[:, 1])**2 +
                          (iron_data[12:, 1] - average_iron[:, 1])**2)

# Построение графика и вывод результата
k_fe, b_fe, dk_fe, db_fe = graphs.plotlsqm(average_iron[:, 0], np.log(average_iron[:, 1]),
                                           np.ones(6) * measurement_error, error_iron / average_iron[:, 1],
                                           title="Логарифмическое ослабление потока для Fe",
                                           xlabel="Толщина образца (мм)",
                                           ylabel="ln(N0 / N)",
                                           bflag=False)
print(f"μ_Fe = ({k_fe * 10:.4f} ± {dk_fe * 10:.4f}) cm^-1")
print(f"hω_Fe = 0.77 MeV")
print()

# Обработка данных для свинца
lead_data = csvreader.readData("pb-data.csv", 0)
lead_data[:, 1] -= ambient_temperature

# Нормализация данных
for series in range(3):
    for index in range(1, 5):
        lead_data[5 * series + index, 0] += lead_data[5 * series + index - 1, 0]
        lead_data[5 * series + index, 1] = lead_data[5 * series, 1] / lead_data[5 * series + index, 1]
    lead_data[5 * series, 1] = 1

# Вычисление среднего значения и погрешности
average_lead = (lead_data[:5, :] + lead_data[5:10, :] + lead_data[10:, :]) / 3
error_lead = 3 * np.sqrt((lead_data[:5, 1] - average_lead[:, 1])**2 +
                          (lead_data[5:10, 1] - average_lead[:, 1])**2 +
                          (lead_data[10:, 1] - average_lead[:, 1])**2)

# Построение графика и вывод результата
k_pb, b_pb, dk_pb, db_pb = graphs.plotlsqm(average_lead[:, 0], np.log(average_lead[:, 1]),
                                           np.ones(5) * measurement_error, error_lead / average_lead[:, 1],
                                           title="Логарифмическое ослабление потока для Pb",
                                           xlabel="Толщина образца (мм)",
                                           ylabel="ln(N0 / N)",
                                           bflag=False)
print(f"μ_Pb = ({k_pb * 10:.3f} ± {dk_pb * 10:.3f}) cm^-1")
print(f"hω_Pb = 0.75 MeV")
print()

# Вычисление среднего значения энергии
average_energy = (0.75 + 0.75 + 0.77) / 3
energy_error = sqrt((0.75 - average_energy)**2 + (0.77 - average_energy)**2 + (0.75 - average_energy)**2)

print(f"hω_avg = ({average_energy:.3f} ± {energy_error:.3f}) MeV")
