import os
import pandas as pd
import streamlit as st
from streamlit_shortcuts import add_shortcuts

# =========================
# CONFIG
# =========================
INPUT_FILE = "mandetta_anotar.csv"
OUTPUT_FILE = "mandetta_anotado.csv"
OPTIONS = ["1 - Conflito", "0 - Não conflito", "-1 - Indeterminado"]

# =========================
# PAGE
# =========================
st.set_page_config(page_title="Anotação de Conflito", layout="wide")

# =========================
# LOAD DF
# =========================
if os.path.exists(OUTPUT_FILE):
    df = pd.read_csv(OUTPUT_FILE)
    st.write("🔄 Continuando anotação existente...")
else:
    df = pd.read_csv(INPUT_FILE)
    st.write("🆕 Criando cópia para anotação...")

if "Conflict" not in df.columns:
    df["Conflict"] = pd.NA

df["Conflict"] = df["Conflict"].astype("Int64")
total = len(df)

# =========================
# HELPERS
# =========================
def label_from_value(value):
    mapping = {
        1: "1 - Conflito",
        0: "0 - Não conflito",
        -1: "-1 - Indeterminado"
    }
    return mapping[int(value)]

def value_from_label(label):
    return int(label.split()[0])

def current_row():
    return df.loc[st.session_state.current_index]

def current_value():
    return df.loc[st.session_state.current_index, "Conflict"]

def save_df():
    df.to_csv(OUTPUT_FILE, index=False)

def set_radio_from_row():
    value = current_value()
    if pd.isna(value):
        st.session_state.classificacao_radio = "0 - Não conflito"
    else:
        st.session_state.classificacao_radio = label_from_value(value)

def push_history(index_before, conflict_before):
    st.session_state.history.append(
        {
            "index": int(index_before),
            "conflict_before": None if pd.isna(conflict_before) else int(conflict_before)
        }
    )

def annotate_current(value, move_next=True):
    i = st.session_state.current_index
    old_value = df.at[i, "Conflict"]
    new_value = int(value)

    if pd.isna(old_value) or int(old_value) != new_value:
        push_history(i, old_value)

    df.at[i, "Conflict"] = new_value
    save_df()

    if move_next and i < total - 1:
        st.session_state.current_index += 1

    set_radio_from_row()

def save_current_from_radio():
    i = st.session_state.current_index
    old_value = df.at[i, "Conflict"]
    new_value = value_from_label(st.session_state.classificacao_radio)

    if pd.isna(old_value) or int(old_value) != new_value:
        push_history(i, old_value)

    df.at[i, "Conflict"] = new_value
    save_df()

def go_prev():
    if st.session_state.current_index > 0:
        st.session_state.current_index -= 1
    set_radio_from_row()

def go_next():
    i = st.session_state.current_index
    new_value = value_from_label(st.session_state.classificacao_radio)
    old_value = df.at[i, "Conflict"]

    if pd.isna(old_value) or int(old_value) != new_value:
        push_history(i, old_value)

    df.at[i, "Conflict"] = new_value
    save_df()

    if i < total - 1:
        st.session_state.current_index += 1

    set_radio_from_row()

def go_next_unlabeled():
    i = st.session_state.current_index
    new_value = value_from_label(st.session_state.classificacao_radio)
    old_value = df.at[i, "Conflict"]

    if pd.isna(old_value) or int(old_value) != new_value:
        push_history(i, old_value)

    df.at[i, "Conflict"] = new_value
    save_df()

    not_done = df[df["Conflict"].isna()].index.tolist()
    next_candidates = [idx for idx in not_done if idx > i]

    if next_candidates:
        st.session_state.current_index = int(next_candidates[0])
    elif not_done:
        st.session_state.current_index = int(not_done[0])

    set_radio_from_row()

def undo_last():
    if not st.session_state.history:
        return

    item = st.session_state.history.pop()
    idx = item["index"]
    prev = item["conflict_before"]

    if prev is None:
        df.at[idx, "Conflict"] = pd.NA
    else:
        df.at[idx, "Conflict"] = prev

    save_df()
    st.session_state.current_index = idx
    set_radio_from_row()

def stop_app():
    save_df()
    st.session_state.stopped = True

# =========================
# SESSION STATE
# =========================
if "current_index" not in st.session_state:
    not_done = df[df["Conflict"].isna()].index.tolist()
    st.session_state.current_index = int(not_done[0]) if not_done else 0

if "history" not in st.session_state:
    st.session_state.history = []

if "classificacao_radio" not in st.session_state:
    value = df.loc[st.session_state.current_index, "Conflict"]
    if pd.isna(value):
        st.session_state.classificacao_radio = "0 - Não conflito"
    else:
        st.session_state.classificacao_radio = label_from_value(value)

if st.session_state.get("last_index_seen") != st.session_state.current_index:
    set_radio_from_row()
    st.session_state.last_index_seen = st.session_state.current_index

# =========================
# SIDEBAR
# =========================
done = int(df["Conflict"].notna().sum())
progress = done / total if total else 0

conflito_count = int((df["Conflict"] == 1).sum())
nao_conflito_count = int((df["Conflict"] == 0).sum())
indeterminado_count = int((df["Conflict"] == -1).sum())
pendentes_count = int(df["Conflict"].isna().sum())

with st.sidebar:
    st.header("Estatísticas")
    st.write(f"Progresso: {done}/{total} ({progress*100:.2f}%)")
    st.write(f"Conflito: {conflito_count}")
    st.write(f"Não conflito: {nao_conflito_count}")
    st.write(f"Indeterminado: {indeterminado_count}")
    st.write(f"Pendentes: {pendentes_count}")

    st.divider()
    st.write("Atalhos:")
    st.write("Z → Conflito")
    st.write("X → Não conflito")
    st.write("V → Indeterminado")
    st.write("Q → Voltar")
    st.write("W → Próximo")
    st.write("E → Salvar")
    st.write("S → Parar")
    st.write("A → Desfazer")
    st.write("N → Próximo não anotado")

# =========================
# MAIN
# =========================
i = st.session_state.current_index
row = current_row()

st.title("Anotação de Conflito")
st.progress(progress)

classe_texto = {
    0: "🟢 Genérico",
    1: "🔵 Reply",
    2: "🟣 Quote"
}.get(row["Class"], "❓ Desconhecido")

st.markdown(f"**Tipo do par:** {classe_texto}")
st.markdown(f"### Item {i+1}/{total}")

valor_atual = row["Conflict"]
if pd.isna(valor_atual):
    st.info("Status atual: ainda não anotado")
elif int(valor_atual) == 1:
    st.success("Status atual: Conflito")
elif int(valor_atual) == 0:
    st.info("Status atual: Não conflito")
else:
    st.warning("Status atual: Indeterminado")

tweet_col1, tweet_col2 = st.columns(2)

with tweet_col1:
    st.markdown("### 🅰️ Tweet 1")
    st.write(row["tweet_1"])

with tweet_col2:
    st.markdown("### 🅱️ Tweet 2")
    st.write(row["tweet_2"])

st.radio(
    "Classificação:",
    OPTIONS,
    key="classificacao_radio",
    horizontal=True
)

st.caption(
    "Atalhos: Z=conflito, X=não conflito, V=indeterminado, "
    "Q=voltar, W=próximo, E=salvar, S=parar, A=desfazer, N=próximo não anotado"
)

nav1, nav2, nav3, nav4 = st.columns(4)

with nav1:
    st.button("⬅️ Voltar (Q)", key="btn_voltar", on_click=go_prev, use_container_width=True)

with nav2:
    st.button("💾 Salvar (E)", key="btn_salvar", on_click=save_current_from_radio, use_container_width=True)

with nav3:
    st.button("➡️ Próximo (W)", key="btn_proximo", on_click=go_next, use_container_width=True)

with nav4:
    st.button("⏭️ Próx. não anotado (N)", key="btn_prox_nao_anotado", on_click=go_next_unlabeled, use_container_width=True)

act1, act2, act3, act4 = st.columns(4)

with act1:
    st.button("Conflito (Z)", key="btn_conflito", on_click=annotate_current, args=(1, True), use_container_width=True)

with act2:
    st.button("Não conflito (X)", key="btn_nao_conflito", on_click=annotate_current, args=(0, True), use_container_width=True)

with act3:
    st.button("Indeterminado (V)", key="btn_indeterminado", on_click=annotate_current, args=(-1, True), use_container_width=True)

with act4:
    st.button("↩️ Desfazer (A)", key="btn_undo", on_click=undo_last, use_container_width=True)

st.button("⛔ Parar (S)", key="btn_parar", on_click=stop_app, use_container_width=True)

# =========================
# SHORTCUTS
# =========================
add_shortcuts(
    btn_conflito="z",
    btn_nao_conflito="x",
    btn_indeterminado="v",
    btn_voltar="q",
    btn_proximo="w",
    btn_salvar="e",
    btn_parar="s",
    btn_undo="a",
    btn_prox_nao_anotado="n",
)

# =========================
# FINAL
# =========================
if st.session_state.get("stopped", False):
    st.warning("Anotação pausada. Pode fechar.")
    st.stop()