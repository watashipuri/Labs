# Подключаем библиотеки для работы с путями, CSV файлами, графиками и математическими операциями
import sys
sys.path.append("../../")
import csvreader
import graphs

import matplotlib.pyplot as plt
import numpy as np

# Чтение данных из файла "data.csv"
data = csvreader.readData("data.csv")

# Калибровочные данные в формате: [энергия, номер канала]
calibration_data = np.array([[1.17, data[0, 0]],
                             [1.33, data[2, 0]],
                             [0.662, data[2, 1]],
                             [1.274, data[2, 2]]])

# Получение коэффициентов для калибровочной линии методом наименьших квадратов
K, B, dK, dB = graphs.plotlsqm(calibration_data[:, 0],
                               calibration_data[:, 1],
                               title="Калибровочный график",
                               xlabel="Энергия фотона, МэВ",
                               ylabel="Номер канала")

# Приведение всех строк данных к энергии (МэВ) на основе полученных коэффициентов
data[0, :] = (data[0, :] - B) / K
data[1, :] = data[1, :] / K
data[2, :] = (data[2, :] - B) / K
data[3, :] = (data[3, :] - B) / K
data[4, :] = (data[4, :] - B) / K

# Вывод скорректированных данных
print("Таблица результатов, приведенная к МэВ:")
print(data)
print()

# Рассчет энергетического разрешения и его погрешности
resolution = data[3, :] / data[2, :]
dResolution = np.sqrt((0.1 / K / data[2, :])**2 + (data[3, :] / data[2, :] * 0.1 / K))
print("Энергетическое разрешение:")
print(resolution)
print("+-", dResolution)
print()

# Определение теоретических энергий для комптоновского рассеяния
mc2 = 0.511  # энергия покоя электрона в МэВ
E_theor = np.array(data[2, :] / (1 + mc2 / (2 * data[2, :])))

# Построение графика экспериментальных и расчетных границ Комптоновского излучения
graphs.plot(E_theor, data[4, :],
            title="Экспериментальные и расчетные границы Комптоновского излучения",
            xlabel="Расчетная энергия, МэВ",
            ylabel="Экспериментальная энергия, МэВ")

# Проверка зависимости R^2 от 1 / E (кроме данных Am)
graphs.plotlsqm(1 / np.concatenate([data[2, :3], [data[2, 4]]]),
                np.concatenate([resolution[:3], [resolution[4]]])**2,
                0.1 / K / np.concatenate([data[2, :3], [data[2, 4]]])**2,
                2 * np.concatenate([resolution[:3], [resolution[4]]]) * np.concatenate([dResolution[:3], [dResolution[4]]]),
                title="Проверка зависимости (6) (кроме Am)",
                xlabel="1 / E, MeV^-1",
                ylabel="Ri^2")

# Чтение данных по Cs137 из двух разных установок
cs137 = csvreader.readData("цезий.csv")
cs137_alt = csvreader.readData("Cs137-alt.csv")

# Построение графиков спектров Cs137 на двух установках
fig, ax = graphs.basePlot()
ax.plot(cs137[:, 0], cs137[:, 1], label="Наши данные")
ax.plot(cs137_alt[:, 0], cs137_alt[:, 1], label="Альтернативные данные")
plt.legend()
plt.title("Спектры цезия-137 на нашей и соседней установках")
plt.xlabel("Канал")
plt.ylabel("Количество фотонов")

# Отображение графика
plt.show()
