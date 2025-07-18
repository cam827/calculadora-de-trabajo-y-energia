import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def calculate_kinetic_energy_translational(mass, velocity):
    """Calcula la energía cinética translacional"""
    return 0.5 * mass * velocity**2

def calculate_kinetic_energy_rotational(moment_inertia, angular_velocity):
    """Calcula la energía cinética rotacional"""
    return 0.5 * moment_inertia * angular_velocity**2

def calculate_potential_energy_gravitational(mass, height, g=9.81):
    """Calcula la energía potencial gravitacional"""
    return mass * g * height

def calculate_potential_energy_elastic(spring_constant, displacement):
    """Calcula la energía potencial elástica"""
    return 0.5 * spring_constant * displacement**2

def calculate_work_constant_force(force, displacement, angle=0):
    """Calcula el trabajo realizado por una fuerza constante"""
    return force * displacement * np.cos(np.radians(angle))

def calculate_work_variable_force(forces, displacements):
    """Calcula el trabajo realizado por una fuerza variable (integración numérica)"""
    return np.trapz(forces, displacements)

def calculate_power(work, time):
    """Calcula la potencia"""
    return work / time if time != 0 else 0

def get_moment_of_inertia(shape, mass, **kwargs):
    """Calcula el momento de inercia para diferentes formas"""
    if shape == "Esfera sólida":
        radius = kwargs.get('radius', 0)
        return (2/5) * mass * radius**2
    elif shape == "Esfera hueca":
        radius = kwargs.get('radius', 0)
        return (2/3) * mass * radius**2
    elif shape == "Cilindro sólido":
        radius = kwargs.get('radius', 0)
        return 0.5 * mass * radius**2
    elif shape == "Cilindro hueco":
        radius = kwargs.get('radius', 0)
        return mass * radius**2
    elif shape == "Barra (eje central)":
        length = kwargs.get('length', 0)
        return (1/12) * mass * length**2
    elif shape == "Barra (extremo)":
        length = kwargs.get('length', 0)
        return (1/3) * mass * length**2
    elif shape == "Disco":
        radius = kwargs.get('radius', 0)
        return 0.5 * mass * radius**2
    else:
        return kwargs.get('custom_I', 0)

def plot_energy_distribution(energies, labels):
    """Crea un gráfico de barras para mostrar la distribución de energía"""
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57']
    bars = ax.bar(labels, energies, color=colors[:len(energies)])
    
    # Añadir valores en las barras
    for bar, energy in zip(bars, energies):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + max(energies)*0.01,
                f'{energy:.2f} J', ha='center', va='bottom', fontweight='bold')
    
    ax.set_ylabel('Energía (J)', fontsize=12)
    ax.set_title('Distribución de Energía', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    return fig

def plot_work_force_diagram(forces, displacements):
    """Crea un gráfico de fuerza vs desplazamiento"""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(displacements, forces, 'b-', linewidth=2, marker='o', markersize=6)
    ax.fill_between(displacements, forces, alpha=0.3, color='lightblue')
    ax.set_xlabel('Desplazamiento (m)', fontsize=12)
    ax.set_ylabel('Fuerza (N)', fontsize=12)
    ax.set_title('Diagrama Fuerza vs Desplazamiento', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Calcular y mostrar el trabajo (área bajo la curva)
    work = np.trapz(forces, displacements)
    ax.text(0.7, 0.8, f'Trabajo = {work:.2f} J', transform=ax.transAxes,
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8),
            fontsize=12, fontweight='bold')
    
    return fig

def main():
    st.set_page_config(page_title="Calculadora de Trabajo y Energía", page_icon="⚡", layout="wide")
    
    st.title("⚡ Calculadora de Trabajo y Energía para Cuerpos Rígidos")
    st.markdown("Esta aplicación calcula diferentes tipos de trabajo y energía para cuerpos rígidos.")
    
    # Barra lateral para navegación
    st.sidebar.title("🔧 Opciones de Cálculo")
    calculation_type = st.sidebar.selectbox(
        "Selecciona el tipo de cálculo:",
        ["Energía Cinética", "Energía Potencial", "Trabajo", "Análisis Completo"]
    )
    
    if calculation_type == "Energía Cinética":
        st.header("🏃 Energía Cinética")
        
        tab1, tab2, tab3 = st.tabs(["Translacional", "Rotacional", "Total"])
        
        with tab1:
            st.subheader("Energía Cinética Translacional")
            st.latex(r"E_{k,trans} = \frac{1}{2}mv^2")
            
            col1, col2 = st.columns(2)
            with col1:
                mass = st.number_input("Masa (kg)", value=1.0, min_value=0.1, format="%.2f")
            with col2:
                velocity = st.number_input("Velocidad (m/s)", value=10.0, format="%.2f")
            
            ek_trans = calculate_kinetic_energy_translational(mass, velocity)
            st.success(f"**Energía Cinética Translacional:** {ek_trans:.2f} J")
        
        with tab2:
            st.subheader("Energía Cinética Rotacional")
            st.latex(r"E_{k,rot} = \frac{1}{2}I\omega^2")
            
            col1, col2 = st.columns(2)
            with col1:
                shape = st.selectbox("Forma del objeto:", [
                    "Esfera sólida", "Esfera hueca", "Cilindro sólido", "Cilindro hueco",
                    "Barra (eje central)", "Barra (extremo)", "Disco", "Personalizado"
                ])
            with col2:
                angular_velocity = st.number_input("Velocidad angular (rad/s)", value=5.0, format="%.2f")
            
            # Parámetros específicos según la forma
            if shape == "Personalizado":
                moment_inertia = st.number_input("Momento de inercia (kg·m²)", value=1.0, format="%.4f")
            else:
                mass_rot = st.number_input("Masa del objeto (kg)", value=1.0, min_value=0.1, format="%.2f")
                if shape in ["Esfera sólida", "Esfera hueca", "Cilindro sólido", "Cilindro hueco", "Disco"]:
                    radius = st.number_input("Radio (m)", value=0.5, min_value=0.01, format="%.2f")
                    moment_inertia = get_moment_of_inertia(shape, mass_rot, radius=radius)
                else:  # Barras
                    length = st.number_input("Longitud (m)", value=1.0, min_value=0.01, format="%.2f")
                    moment_inertia = get_moment_of_inertia(shape, mass_rot, length=length)
            
            ek_rot = calculate_kinetic_energy_rotational(moment_inertia, angular_velocity)
            st.info(f"**Momento de Inercia:** {moment_inertia:.4f} kg·m²")
            st.success(f"**Energía Cinética Rotacional:** {ek_rot:.2f} J")
        
        with tab3:
            st.subheader("Energía Cinética Total")
            st.latex(r"E_{k,total} = E_{k,trans} + E_{k,rot}")
            
            # Usar valores de las pestañas anteriores si existen
            try:
                ek_total = ek_trans + ek_rot
                st.success(f"**Energía Cinética Total:** {ek_total:.2f} J")
                
                # Gráfico de distribución
                energies = [ek_trans, ek_rot, ek_total]
                labels = ['Translacional', 'Rotacional', 'Total']
                fig = plot_energy_distribution(energies, labels)
                st.pyplot(fig)
                
            except:
                st.warning("Complete los cálculos en las pestañas anteriores para ver el total.")
    
    elif calculation_type == "Energía Potencial":
        st.header("⛰️ Energía Potencial")
        
        tab1, tab2 = st.tabs(["Gravitacional", "Elástica"])
        
        with tab1:
            st.subheader("Energía Potencial Gravitacional")
            st.latex(r"E_{p,grav} = mgh")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                mass_grav = st.number_input("Masa (kg)", value=1.0, min_value=0.1, format="%.2f", key="mass_grav")
            with col2:
                height = st.number_input("Altura (m)", value=10.0, format="%.2f")
            with col3:
                g = st.number_input("Aceleración gravitacional (m/s²)", value=9.81, format="%.2f")
            
            ep_grav = calculate_potential_energy_gravitational(mass_grav, height, g)
            st.success(f"**Energía Potencial Gravitacional:** {ep_grav:.2f} J")
        
        with tab2:
            st.subheader("Energía Potencial Elástica")
            st.latex(r"E_{p,elast} = \frac{1}{2}kx^2")
            
            col1, col2 = st.columns(2)
            with col1:
                spring_constant = st.number_input("Constante del resorte (N/m)", value=100.0, format="%.2f")
            with col2:
                displacement = st.number_input("Desplazamiento (m)", value=0.5, format="%.2f")
            
            ep_elastic = calculate_potential_energy_elastic(spring_constant, displacement)
            st.success(f"**Energía Potencial Elástica:** {ep_elastic:.2f} J")
    
    elif calculation_type == "Trabajo":
        st.header("🔨 Trabajo")
        
        tab1, tab2 = st.tabs(["Fuerza Constante", "Fuerza Variable"])
        
        with tab1:
            st.subheader("Trabajo por Fuerza Constante")
            st.latex(r"W = F \cdot d \cdot \cos(\theta)")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                force = st.number_input("Fuerza (N)", value=50.0, format="%.2f")
            with col2:
                displacement_const = st.number_input("Desplazamiento (m)", value=5.0, format="%.2f", key="disp_const")
            with col3:
                angle = st.number_input("Ángulo (grados)", value=0.0, format="%.2f")
            
            work_const = calculate_work_constant_force(force, displacement_const, angle)
            st.success(f"**Trabajo realizado:** {work_const:.2f} J")
            
            # Mostrar información adicional
            st.info(f"""
            **Cálculo detallado:**
            - Fuerza: {force} N
            - Desplazamiento: {displacement_const} m
            - Ángulo: {angle}°
            - cos({angle}°) = {np.cos(np.radians(angle)):.4f}
            - Trabajo = {force} × {displacement_const} × {np.cos(np.radians(angle)):.4f} = {work_const:.2f} J
            """)
        
        with tab2:
            st.subheader("Trabajo por Fuerza Variable")
            st.latex(r"W = \int F \cdot dx")
            
            # Opciones para definir la fuerza variable
            force_type = st.selectbox("Tipo de fuerza:", ["Lineal", "Cuadrática", "Datos personalizados"])
            
            if force_type == "Lineal":
                st.write("Fuerza = a × x + b")
                col1, col2, col3 = st.columns(3)
                with col1:
                    a = st.number_input("Coeficiente a", value=10.0, format="%.2f")
                with col2:
                    b = st.number_input("Coeficiente b", value=0.0, format="%.2f")
                with col3:
                    x_max = st.number_input("Desplazamiento máximo (m)", value=5.0, format="%.2f")
                
                x_vals = np.linspace(0, x_max, 100)
                forces = a * x_vals + b
                
            elif force_type == "Cuadrática":
                st.write("Fuerza = a × x² + b × x + c")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    a = st.number_input("Coeficiente a", value=1.0, format="%.2f", key="a_quad")
                with col2:
                    b = st.number_input("Coeficiente b", value=0.0, format="%.2f", key="b_quad")
                with col3:
                    c = st.number_input("Coeficiente c", value=0.0, format="%.2f")
                with col4:
                    x_max = st.number_input("Desplazamiento máximo (m)", value=5.0, format="%.2f", key="x_max_quad")
                
                x_vals = np.linspace(0, x_max, 100)
                forces = a * x_vals**2 + b * x_vals + c
                
            else:  # Datos personalizados
                st.write("Ingresa los datos de fuerza y desplazamiento:")
                
                # Crear una tabla editable
                n_points = st.number_input("Número de puntos", value=5, min_value=2, max_value=20)
                
                data = []
                for i in range(n_points):
                    col1, col2 = st.columns(2)
                    with col1:
                        x = st.number_input(f"x_{i+1} (m)", value=float(i), format="%.2f", key=f"x_{i}")
                    with col2:
                        f = st.number_input(f"F_{i+1} (N)", value=10.0, format="%.2f", key=f"f_{i}")
                    data.append([x, f])
                
                df = pd.DataFrame(data, columns=['Desplazamiento (m)', 'Fuerza (N)'])
                x_vals = df['Desplazamiento (m)'].values
                forces = df['Fuerza (N)'].values
            
            # Calcular el trabajo
            work_var = calculate_work_variable_force(forces, x_vals)
            st.success(f"**Trabajo realizado:** {work_var:.2f} J")
            
            # Mostrar gráfico
            fig = plot_work_force_diagram(forces, x_vals)
            st.pyplot(fig)
    
    else:  # Análisis Completo
        st.header("📊 Análisis Completo de Trabajo y Energía")
        
        st.subheader("Parámetros del Sistema")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Propiedades del Objeto:**")
            mass_total = st.number_input("Masa (kg)", value=2.0, min_value=0.1, format="%.2f", key="mass_total")
            shape_total = st.selectbox("Forma:", [
                "Esfera sólida", "Cilindro sólido", "Disco", "Barra (eje central)"
            ], key="shape_total")
            
            if shape_total in ["Esfera sólida", "Cilindro sólido", "Disco"]:
                radius_total = st.number_input("Radio (m)", value=0.3, format="%.2f", key="radius_total")
                I_total = get_moment_of_inertia(shape_total, mass_total, radius=radius_total)
            else:
                length_total = st.number_input("Longitud (m)", value=1.0, format="%.2f", key="length_total")
                I_total = get_moment_of_inertia(shape_total, mass_total, length=length_total)
        
        with col2:
            st.write("**Estado Cinemático:**")
            v_total = st.number_input("Velocidad translacional (m/s)", value=5.0, format="%.2f", key="v_total")
            omega_total = st.number_input("Velocidad angular (rad/s)", value=3.0, format="%.2f", key="omega_total")
            h_total = st.number_input("Altura (m)", value=5.0, format="%.2f", key="h_total")
        
        # Calcular todas las energías
        ek_trans_total = calculate_kinetic_energy_translational(mass_total, v_total)
        ek_rot_total = calculate_kinetic_energy_rotational(I_total, omega_total)
        ep_grav_total = calculate_potential_energy_gravitational(mass_total, h_total)
        
        total_energy = ek_trans_total + ek_rot_total + ep_grav_total
        
        # Mostrar resultados
        st.subheader("Resultados del Análisis")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("E. Cinética Translacional", f"{ek_trans_total:.2f} J")
        with col2:
            st.metric("E. Cinética Rotacional", f"{ek_rot_total:.2f} J")
        with col3:
            st.metric("E. Potencial Gravitacional", f"{ep_grav_total:.2f} J")
        with col4:
            st.metric("Energía Total", f"{total_energy:.2f} J")
        
        # Gráfico de distribución de energía
        energies = [ek_trans_total, ek_rot_total, ep_grav_total]
        labels = ['E. Cinética\nTranslacional', 'E. Cinética\nRotacional', 'E. Potencial\nGravitacional']
        fig = plot_energy_distribution(energies, labels)
        st.pyplot(fig)
        
        # Información adicional
        st.subheader("Información Adicional")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"""
            **Propiedades Calculadas:**
            - Momento de inercia: {I_total:.4f} kg·m²
            - Energía cinética total: {ek_trans_total + ek_rot_total:.2f} J
            - Porcentaje de E.C. translacional: {(ek_trans_total/total_energy)*100:.1f}%
            - Porcentaje de E.C. rotacional: {(ek_rot_total/total_energy)*100:.1f}%
            """)
        
        with col2:
            st.info(f"""
            **Conversiones de Energía:**
            - Velocidad equivalente (solo translacional): {np.sqrt(2*total_energy/mass_total):.2f} m/s
            - Altura equivalente (solo potencial): {total_energy/(mass_total*9.81):.2f} m
            - Velocidad angular equivalente: {np.sqrt(2*total_energy/I_total):.2f} rad/s
            """)
    
    # Información teórica
    with st.expander("📚 Información Teórica"):
        st.markdown("""
        ## Conceptos Fundamentales
        
        ### Energía Cinética
        - **Translacional**: Energía debido al movimiento lineal del centro de masa
        - **Rotacional**: Energía debido al movimiento de rotación alrededor de un eje
        
        ### Energía Potencial
        - **Gravitacional**: Energía almacenada debido a la posición en un campo gravitacional
        - **Elástica**: Energía almacenada en sistemas elásticos (resortes, materiales deformables)
        
        ### Trabajo
        - **Definición**: Energía transferida a un objeto cuando una fuerza actúa sobre él
        - **Teorema trabajo-energía**: El trabajo neto realizado sobre un objeto es igual al cambio en su energía cinética
        
        ### Momento de Inercia
        El momento de inercia depende de la forma del objeto y el eje de rotación:
        - **Esfera sólida**: I = (2/5)mr²
        - **Cilindro sólido**: I = (1/2)mr²
        - **Disco**: I = (1/2)mr²
        - **Barra (centro)**: I = (1/12)ml²
        """)

if __name__ == "__main__":
    main()
    