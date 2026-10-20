"""
Motor de Cálculo do INSS Progressivo (Vigência 2026)
Fundamento Legal:
- EC 103/2019 (Art. 28 - Progressividade das alíquotas)
- Decreto nº 12.797/2025 (Salário Mínimo Nacional 2026: R$ 1.621,00)
- Portaria Interministerial MPS/MF nº 13, de 09/01/2026 (Tabela e Teto R$ 8.475,55)
"""

SALARIO_MINIMO_2026 = 1621.00
TETO_INSS_2026 = 8475.55

# Tabela oficial 2026: (limite_superior_da_faixa, aliquota, parcela_a_deduzir)
FAIXAS_INSS_2026 = [
    (1621.00, 0.075, 0.00),     # 1ª Faixa: até R$ 1.621,00 (7,5%)
    (2902.84, 0.090, 24.32),    # 2ª Faixa: de R$ 1.621,01 até R$ 2.902,84 (9,0%)
    (4354.27, 0.120, 111.40),   # 3ª Faixa: de R$ 2.902,85 até R$ 4.354,27 (12,0%)
    (8475.55, 0.140, 198.49),   # 4ª Faixa: de R$ 4.354,28 até R$ 8.475,55 (14,0%)
]


def calcular_inss_2026(salario_bruto: float) -> dict:
    desconto_total = 0.0
    limite_anterior = 0.0
    extrato_faixas = []

    for indice, (teto_faixa, aliquota, _) in enumerate(FAIXAS_INSS_2026, start=1):
        if salario_bruto > limite_anterior:
            # Fatiamento: tributa apenas a porção do salário que cabe nesta faixa
            base_faixa = min(salario_bruto, teto_faixa) - limite_anterior
            desconto_faixa = base_faixa * aliquota
            desconto_total += desconto_faixa

            extrato_faixas.append({
                "faixa": f"{indice}ª Faixa",
                "intervalo": f"R$ {limite_anterior + 0.01 if limite_anterior > 0 else 0.00:,.2f} a R$ {teto_faixa:,.2f}",
                "aliquota_pct": aliquota * 100,
                "base_calculada": round(base_faixa, 2),
                "desconto": round(desconto_faixa, 2)
            })
            limite_anterior = teto_faixa
        else:
            break

    desconto_final = round(desconto_total, 2)
    aliquota_efetiva = (desconto_final / salario_bruto * 100) if salario_bruto > 0 else 0.0
    atingiu_teto = salario_bruto >= TETO_INSS_2026
    qtd_salarios_minimos = salario_bruto / SALARIO_MINIMO_2026

    return {
        "salario_bruto": round(salario_bruto, 2),
        "qtd_salarios_minimos": round(qtd_salarios_minimos, 2),
        "desconto_inss": desconto_final,
        "salario_base_irrf": round(salario_bruto - desconto_final, 2),
        "aliquota_efetiva": round(aliquota_efetiva, 2),
        "atingiu_teto": atingiu_teto,
        "parcela_isenta_teto": round(max(0.0, salario_bruto - TETO_INSS_2026), 2),
        "detalhes": extrato_faixas
    }


def main():
    print("=" * 68)
    print("   DEPARTAMENTO PESSOAL: CALCULADORA DE INSS 2026 (PORTARIA 13/26)  ")
    print("=" * 68)
    print(f"• Salário Mínimo Vigente: R$ {SALARIO_MINIMO_2026:,.2f}")
    print(f"• Teto do RGPS/INSS 2026: R$ {TETO_INSS_2026:,.2f} (Desconto máx: R$ 988,09)")
    print("-" * 68)

    try:
        entrada = input("Informe o salário bruto do colaborador (R$): ").strip()
        salario = float(entrada.replace(".", "").replace(",", "."))

        if salario <= 0:
            print("Erro: O valor do salário deve ser maior que zero.")
            return

        if salario < SALARIO_MINIMO_2026:
            print(
                f"\n[ATENÇÃO RH] O valor informado é inferior ao piso nacional de "
                f"R$ {SALARIO_MINIMO_2026:.2f} (salvo jornada parcial/aprendiz)."
            )

        res = calcular_inss_2026(salario)

        print("\n" + "-" * 68)
        print("MEMÓRIA DE CÁLCULO PROGRESSIVO (FATIA POR FATIA):")
        for item in res["detalhes"]:
            print(
                f"• {item['faixa']} ({item['aliquota_pct']:>4.1f}%): "
                f"Base R$ {item['base_calculada']:>8.2f}  -->  INSS: R$ {item['desconto']:>6.2f}"
            )

        if res["atingiu_teto"]:
            print(
                f"• [TETO ATINGIDO] R$ {res['parcela_isenta_teto']:>8.2f} excedentes ao teto "
                f"de R$ {TETO_INSS_2026:.2f} não sofrem desconto do segurado."
            )

        print("-" * 68)
        print(f"Salário Bruto Informado:     R$ {res['salario_bruto']:>10.2f} ({res['qtd_salarios_minimos']}x SM)")
        print(f"Desconto Total do INSS:      R$ {res['desconto_inss']:>10.2f}")
        print(f"Alíquota Efetiva Real:          {res['aliquota_efetiva']:>10.2f}%")
        print(f"Base Líquida p/ IRRF:        R$ {res['salario_base_irrf']:>10.2f}")
        print("=" * 68)

    except ValueError:
        print("Erro: Digite um valor numérico válido (ex: 5000.00 ou 5.000,00).")


if __name__ == "__main__":
    main()