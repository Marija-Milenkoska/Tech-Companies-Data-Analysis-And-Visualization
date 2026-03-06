import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

data = pd.read_csv("tech_companies.csv")

print("HEAD:")
print(data.head(), "\n")

print("INFO:")
print(data.info(), "\n")

print("NaN VALUES:")
print(data.isna().sum(), "\n")

print("DUPLICATES:")
print(data.duplicated().sum(), "\n")

print("ROWS PER COMPANY:")
print(data["Company"].value_counts(), "\n")

print("YEAR RANGE:")
print(data["Year"].min(), data["Year"].max(), "\n")

year_company_covarage = data.pivot_table(
    index="Year",
    columns="Company",
    values="Revenue_in_Billions",
    aggfunc="size"
)
print("YEAR-COMPANY COVERAGE:")
print(year_company_covarage, "\n")

num_columns = data.select_dtypes(include=['float64','int64']).columns
negative_vals = {col: (data[col] < 0).sum() for col in num_columns}
print("NEGATIVE VALUES PER COLUMN:")
print(negative_vals, "\n")

print("NEGATIVE VALUES PER ROW:")
print(data[data["NetIncome_in_Billions"] < 0][
    ["Company", "Year", "NetIncome_in_Billions", "Profit_Margin_pct"]
])
print("DESCRIBE:")
print(data.describe(), "\n")

print("AVERAGE REVENUE PER COMPANY :")
print(data.groupby("Company")["Revenue_in_Billions"].mean(), "\n")

print("AVERAGE REVENUE, NET INCOME AND R&D PER COMPANY :")
print(data.groupby("Company")[["Revenue_in_Billions",
                             "NetIncome_in_Billions",
                             "R&D_in_Billions"]].mean(), "\n")
print(data.groupby("Company")["Profit_Margin_pct"].mean())

data_sorted = data.sort_values(["Company", "Year"])

data_sorted["Revenue_growth"] = data_sorted.groupby("Company")["Revenue_in_Billions"].diff()

print("REVENUE GROWTH PER COMPANY:")
print(data_sorted[["Company", "Year", "Revenue_in_Billions", "Revenue_growth"]])

print("BEST REVENUE GROWTH PER COMPANY:")
print(data_sorted.loc[data_sorted.groupby("Company")["Revenue_growth"].idxmax(),
                    ["Company", "Year", "Revenue_growth"]])

print("WORST REVENUE DECLINE PER COMPANY:")
print(data_sorted.loc[data_sorted.groupby("Company")["Revenue_growth"].idxmin(),
                    ["Company", "Year", "Revenue_growth"]])

print("CORRELATION: ")
correlation_table = data.corr(numeric_only=True)
print(correlation_table)



#Visualization part

plt.figure(figsize=(12, 6))
sns.lineplot(data=data, x="Year", y="Revenue_in_Billions", hue="Company", marker="o")
plt.title("ПРИХОДИ НА ТЕХНОЛОШКИ КОМПАНИИ (2010–2025)", fontsize=14)
plt.xlabel("Година")
plt.ylabel("Приход (милијарди $)")
plt.grid(True)
plt.tight_layout()
plt.savefig("revenues.png")

plt.figure(figsize=(12, 6))
sns.lineplot(
    data=data,
    x="Year",
    y="Profit_Margin_pct",
    hue="Company",
    marker="o"
)
plt.title("ПРОФИТНА МАРЖА НА ТЕХНОЛОШКИТЕ КОМПАНИИ (2011–2025)")
plt.xlabel("Година")
plt.ylabel("Профитна маржа (%)")
plt.grid(True)
plt.tight_layout()
plt.savefig("profit_margin.png")

plt.figure(figsize=(12, 6))
sns.lineplot(
    data=data,
    x="Year",
    y="R&D_in_Billions",
    hue="Company",
    marker="o"
)
plt.title("ИНВЕСТИЦИИ ЗА ИСТРАЖУВАЊЕ И РАЗВОЈ НА ТЕХНОЛОШКИТЕ КОМПАНИИ (2011–2025)")
plt.xlabel("Година")
plt.ylabel("R&D инвестиции (милијарди $)")
plt.grid(True)
plt.tight_layout()
plt.savefig("rnd_investments.png")

plt.figure(figsize=(12, 6))
sns.lineplot(
    data=data,
    x="Year",
    y="R&D_pct_of_Revenue",
    hue="Company",
    marker="o"
)
plt.title("ПРОЦЕНТ НА R&D ВЛОЖУВАЊА(2011–2025)")
plt.xlabel("Година")
plt.ylabel("R&D како % од приходите")
plt.grid(True)
plt.tight_layout()
plt.savefig("rnd_percentage.png")

plt.figure(figsize=(12, 6))
sns.lineplot(
    data=data,
    x="Year",
    y="Employees",
    hue="Company",
    marker="o"
)
plt.title("БРОЈ НА ВРАБОТЕНИ ВО ТЕХНОЛОШКИТЕ КОМПАНИИ (2011–2025)")
plt.xlabel("Година")
plt.ylabel("Број на вработени")
plt.grid(True)
plt.tight_layout()
plt.savefig("employees.png")


latest_year = data.groupby("Company")["Year"].max().min()
data_latest = data[data["Year"] == latest_year]
plt.figure(figsize=(12, 6))
sns.barplot(
    data=data_latest,
    x="Company",
    y="Revenue_in_Billions",
    hue="Company",
    palette="viridis",
    legend=False
)
plt.title(f"ПРИХОДИ НА ТЕХНОЛОШКИТЕ КОМПАНИИ ВО  {latest_year} ГОДИНА")
plt.xlabel("Компанија")
plt.ylabel("Приход (милијарди $)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("revenue_bar_latest_year.png")

full_year = data.groupby("Company")["Year"].max().min()
data_full_year = data[data["Year"] == full_year]
plt.figure(figsize=(8, 8))
plt.pie(
    data_full_year["Revenue_in_Billions"],
    labels=data_full_year["Company"],
    autopct="%1.1f%%",
    startangle=90
)
plt.title(f"ПРИХОДИ НА ТЕХНОЛОШКИТЕ КОМПАНИИ ВО {full_year} ГОДИНА")
plt.tight_layout()
plt.savefig(f"revenue_pie_latest_year.png")

plt.figure(figsize=(12, 8))
sns.heatmap(
    correlation_table,
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)
plt.title("КОРЕЛАЦИСКА МАТРИЦА")
plt.tight_layout()
plt.savefig("correlation_heatmap.png")

common_year = data.groupby("Company")["Year"].max().min()
sankey_data = data[data["Year"] == common_year].copy()

for _, row in sankey_data.iterrows():
    company = row["Company"]
    revenue = row["Revenue_in_Billions"]
    operating_income = row["OperatingIncome_in_Billions"]
    net_income = row["NetIncome_in_Billions"]
    rnd = row["R&D_in_Billions"]

    operating_costs = max(revenue - operating_income, 0)
    other_operating_costs = max(operating_costs - rnd, 0)
    other_non_operating = max(operating_income - net_income, 0)

    labels = [
        f"{company} Revenue",
        f"{company} Operating Costs",
        f"{company} Operating Income",
        f"{company} R&D",
        f"{company} Other Operating Costs",
        f"{company} Net Income",
        f"{company} Other Non-Operating / Tax"
    ]

    source = [0,0,1,1,2,2]
    target = [1,2,3,4,5,6]

    values = [
        operating_costs,
        operating_income,
        rnd,
        other_operating_costs,
        net_income,
        other_non_operating
    ]

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=20,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels
        ),
        link=dict(
            source=source,
            target=target,
            value=values
        )
    )])

    fig.update_layout(
        title_text=f"ФИНАНСИСКА СТРУКТУРА НА {company}",
        font_size=11,
        width=1200,
        height=700
    )

    fig.write_image(f"sankey_{company.lower().replace(' ', '_')}.png")
