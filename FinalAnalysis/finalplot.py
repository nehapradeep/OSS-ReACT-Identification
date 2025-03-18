import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("ReACTCounts.csv", header=None)


df = df.T
df.columns = ["Count", "React"]
df = df.iloc[1:].reset_index(drop=True)


df["Count"] = pd.to_numeric(df["Count"], errors="coerce").astype(int)


df["Color"] = df["Count"].apply(lambda x: "#1e5f82" if x > 7 else "#66b3e0")


fig = go.Figure()

for _, row in df.iterrows():
    fig.add_trace(go.Bar(
        x=[row["React"]],
        y=[row["Count"]],
        marker_color=row["Color"],
        name=row["React"]
    ))


for _, row in df.iterrows():
    if row["Count"] > 7:
        react_number = row["React"].split("-")[-1]
        fig.add_annotation(
            x=row["React"],
            y=row["Count"] + 1, 
            text=f"ReACT-{react_number}",
            showarrow=False,
            font=dict(color="#1e5f82", size=12),
            textangle=-90 
        )

# Add red dashed threshold line at y=7
fig.add_shape(
    type="line",
    x0=-0.5, x1=len(df) - 0.5, 
    y0=7, y1=7, 
    line=dict(color="red", width=2, dash="dash")
)

# Layout adjustments
fig.update_layout(
    title="Total Count of Each ReACT",
    xaxis_title="ReACT Types",
    yaxis_title="Count",
    showlegend=False
)

fig.show()
