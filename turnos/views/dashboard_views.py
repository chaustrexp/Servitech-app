from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from datetime import date, timedelta
import calendar

from ..models import Cita, Usuario, Repuesto, Servicio, Especialidad
from ..forms import EditarPerfilForm


# ─────────────────────────────────────────────
#  DASHBOARD ADMINISTRADOR
# ─────────────────────────────────────────────
@login_required
def admin_dashboard(request):
    """Dashboard principal del administrador con métricas reales."""
    if request.user.rol != Usuario.Rol.ADMINISTRADOR:
        return redirect('home')

    hoy = date.today()

    # ── KPIs ──
    total_citas     = Cita.objects.filter(fecha__year=hoy.year, fecha__month=hoy.month).count()
    total_tecnicos  = Usuario.objects.filter(rol=Usuario.Rol.TECNICO, activo=True).count()
    total_usuarios  = Usuario.objects.filter(activo=True).count()
    total_servicios = Servicio.objects.filter(activo=True).count()

    # Citas de hoy
    citas_hoy = Cita.objects.filter(fecha=hoy).count()

    # ── Actividad reciente (últimas 6 citas) ──
    actividad_reciente = (
        Cita.objects
        .select_related('cliente', 'servicio', 'estado', 'tecnico')
        .order_by('-fecha_creacion')[:6]
    )

    # ── Repuestos con stock bajo (menos de 3 unidades) ──
    stock_bajo = Repuesto.objects.filter(activo=True, stock__lt=3).order_by('stock')[:3]

    # ── Tendencias por día de la semana (semana actual) ──
    inicio_semana = hoy - timedelta(days=hoy.weekday())  # lunes
    tendencias = []
    dias_label = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
    for i in range(7):
        dia = inicio_semana + timedelta(days=i)
        total_dia = Cita.objects.filter(fecha=dia).count()
        finalizadas_dia = Cita.objects.filter(fecha=dia, estado__nombre__iexact='Finalizada').count()
        tendencias.append({
            'label': dias_label[i],
            'total': total_dia,
            'finalizadas': finalizadas_dia,
            'es_hoy': dia == hoy,
        })

    # Máximo para calcular porcentajes de las barras
    max_tendencia = max((t['total'] for t in tendencias), default=1) or 1

    context = {
        'total_citas':        total_citas,
        'total_tecnicos':     total_tecnicos,
        'total_usuarios':     total_usuarios,
        'total_servicios':    total_servicios,
        'citas_hoy':          citas_hoy,
        'actividad_reciente': actividad_reciente,
        'stock_bajo':         stock_bajo,
        'tendencias':         tendencias,
        'max_tendencia':      max_tendencia,
    }
    return render(request, 'turnos/administracion/admin_dashboard.html', context)

@login_required
def dashboard_tecnico(request):
    """Dashboard del técnico: obtiene citas reales desde la base de datos PostgreSQL."""
    if request.user.rol != Usuario.Rol.TECNICO:
        return redirect('home')

    from datetime import date
    hoy = date.today()

    # Citas programadas para hoy
    citas_hoy_count = Cita.objects.filter(fecha=hoy).count()

    # Citas en proceso (En diagnóstico o En reparación)
    en_proceso_count = Cita.objects.filter(
        estado__nombre__in=['EN_DIAGNOSTICO', 'EN_REPARACION', 'En Diagnóstico', 'En Reparación']
    ).count()

    # Citas finalizadas
    finalizadas_count = Cita.objects.filter(
        estado__nombre__iexact='finalizada'
    ).count()

    # Citas con retraso
    retrasos_count = Cita.objects.filter(
        estado__nombre__iexact='retrasada'
    ).count()

    # Citas disponibles para tomar: sin técnico asignado, en estado PENDIENTE, CONFIRMADA o REAGENDADA
    ESTADOS_DISPONIBLES = [
        'PENDIENTE', 'Pendiente', 'pendiente',
        'CONFIRMADA', 'Confirmada', 'confirmada',
        'REAGENDADA', 'Reagendada', 'reagendada',
    ]
    citas_disponibles = Cita.objects.filter(
        estado__nombre__in=ESTADOS_DISPONIBLES,
        tecnico__isnull=True
    ).select_related('cliente', 'servicio', 'estado').order_by('fecha', 'hora_inicio')

    context = {
        'citas_hoy_count': citas_hoy_count,
        'en_proceso_count': en_proceso_count,
        'finalizadas_count': finalizadas_count,
        'retrasos_count': retrasos_count,
        'citas_disponibles': citas_disponibles,
        'total_disponibles': citas_disponibles.count(),
        'hoy': hoy,
    }
    return render(request, 'turnos/tecnico/tecnico_inicio.html', context)

@login_required
def tecnico_agenda(request):
    """Agenda del técnico."""
    if request.user.rol != Usuario.Rol.TECNICO:
        return redirect('home')
    return render(request, 'turnos/tecnico/tecnico_agenda.html')

@login_required
def tecnico_dispositivos(request):
    """Gestión de dispositivos e inventario para el técnico."""
    if request.user.rol != Usuario.Rol.TECNICO:
        return redirect('home')

    # Si no hay repuestos registrados, creamos algunos datos iniciales (semilla integrada)
    if Repuesto.objects.count() == 0:
        initial_repuestos = [
            ("Pantalla iPhone 14", "OLED Original Apple", "PANTALLAS", 12, 289.00),
            ("Batería Samsung S22", "3700mAh Li-ion", "BATERIAS", 2, 45.50),
            ("Puerto Carga MacBook Pro", "MagSafe 3 Assembly", "CONECTORES", 5, 112.00),
            ("Módulo Cámara Pixel 7", "Sensor Principal 50MP", "CAMARAS", 0, 98.00),
        ]
        for name, desc, cat, stock, price in initial_repuestos:
            Repuesto.objects.create(nombre=name, descripcion=desc, categoria=cat, stock=stock, precio=price)

    repuestos = Repuesto.objects.filter(activo=True).order_by('-fecha_registro')
    return render(request, 'turnos/tecnico/tecnico_dispositivos.html', {'repuestos': repuestos})

@login_required
def tecnico_clientes(request):
    """Directorio de clientes para el técnico: muestra todos los clientes registrados."""
    if request.user.rol != Usuario.Rol.TECNICO:
        return redirect('home')

    from django.db.models import Count, Max, Subquery, OuterRef
    from turnos.models.citas import Cita

    # Subquery: nombre del último servicio de cada cliente
    ultimo_servicio_sq = (
        Cita.objects
        .filter(cliente=OuterRef('pk'))
        .order_by('-fecha', '-hora_inicio')
        .values('servicio__nombre')[:1]
    )

    clientes = (
        Usuario.objects
        .filter(rol=Usuario.Rol.CLIENTE)
        .annotate(
            total_citas=Count('citas_cliente', distinct=True),
            ultima_fecha=Max('citas_cliente__fecha'),
            ultimo_servicio=Subquery(ultimo_servicio_sq),
        )
        .order_by('-total_citas', 'nombre_completo')
    )

    # Clasificación de nivel según cantidad de citas
    def nivel_cliente(citas):
        if citas >= 8:
            return {'label': 'Platinum', 'bg': 'bg-purple-100', 'text': 'text-purple-700'}
        elif citas >= 4:
            return {'label': 'Gold', 'bg': 'bg-yellow-100', 'text': 'text-yellow-700'}
        elif citas >= 2:
            return {'label': 'Silver', 'bg': 'bg-slate-100', 'text': 'text-slate-600'}
        else:
            return {'label': 'Nuevo', 'bg': 'bg-emerald-100', 'text': 'text-emerald-700'}

    # Agregar nivel a cada cliente (como atributo dinámico)
    clientes_con_nivel = []
    for c in clientes:
        c.nivel = nivel_cliente(c.total_citas)
        c.tag_filtro = _tag_filtro(c)
        clientes_con_nivel.append(c)

    total_clientes = len(clientes_con_nivel)
    nuevos_mes = sum(
        1 for c in clientes_con_nivel
        if c.fecha_registro and c.fecha_registro.month == __import__('datetime').date.today().month
    )

    context = {
        'clientes': clientes_con_nivel,
        'total_clientes': total_clientes,
        'nuevos_mes': nuevos_mes,
    }
    return render(request, 'turnos/tecnico/tecnico_clientes.html', context)


def _tag_filtro(cliente):
    """Genera las etiquetas de filtro (recientes, fieles, inactivos) para data-tag."""
    import datetime
    tags = []
    hoy = datetime.date.today()

    if cliente.ultima_fecha:
        dias = (hoy - cliente.ultima_fecha).days
        if dias <= 30:
            tags.append('recientes')
        elif dias > 90:
            tags.append('inactivos')

    if cliente.total_citas >= 3:
        tags.append('fieles')

    return ' '.join(tags) if tags else 'todos'



@login_required
def tecnico_soporte(request):
    """Soporte operativo para el técnico."""
    if request.user.rol != Usuario.Rol.TECNICO:
        return redirect('home')
    return render(request, 'turnos/tecnico/tecnico_soporte.html')


@login_required
def tecnico_reporte_mensual(request):
    """
    Genera el reporte mensual del técnico como archivo Excel (.xlsx).
    Parámetros GET: mes (1-12), anio (ej. 2026)
    """
    from datetime import date
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from django.http import HttpResponse

    if request.user.rol != Usuario.Rol.TECNICO:
        return redirect('home')

    hoy = date.today()
    try:
        mes  = int(request.GET.get('mes',  hoy.month))
        anio = int(request.GET.get('anio', hoy.year))
        if not (1 <= mes <= 12):  mes  = hoy.month
        if not (2000 <= anio <= 2100): anio = hoy.year
    except (ValueError, TypeError):
        mes, anio = hoy.month, hoy.year

    MESES_ES = {
        1:'Enero', 2:'Febrero', 3:'Marzo', 4:'Abril',
        5:'Mayo',  6:'Junio',   7:'Julio', 8:'Agosto',
        9:'Septiembre', 10:'Octubre', 11:'Noviembre', 12:'Diciembre',
    }
    nombre_mes = MESES_ES.get(mes, str(mes))

    citas = (
        Cita.objects
        .filter(tecnico=request.user, fecha__year=anio, fecha__month=mes)
        .select_related('cliente', 'servicio', 'estado')
        .order_by('fecha', 'hora_inicio')
    )

    total      = citas.count()
    finalizadas = citas.filter(estado__nombre__iexact='finalizada').count()
    canceladas  = citas.filter(estado__nombre__iexact='cancelada').count()
    pendientes  = citas.exclude(estado__nombre__in=['Finalizada','Cancelada','FINALIZADA','CANCELADA']).count()
    tasa        = f"{round(finalizadas / total * 100, 1)}%" if total > 0 else "0%"

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Reporte de Servicios"

    # Habilitar cuadrícula visible
    ws.views.sheetView[0].showGridLines = True

    # Estilos
    font_title = Font(name='Arial', size=14, bold=True, color='FFFFFF')
    font_section = Font(name='Arial', size=11, bold=True, color='002B75')
    font_header = Font(name='Arial', size=10, bold=True, color='FFFFFF')
    font_body = Font(name='Arial', size=10)
    font_bold = Font(name='Arial', size=10, bold=True)
    
    fill_navy = PatternFill(start_color='002B75', end_color='002B75', fill_type='solid')
    fill_light_blue = PatternFill(start_color='EEF2FF', end_color='EEF2FF', fill_type='solid')
    fill_gray = PatternFill(start_color='F8FAFC', end_color='F8FAFC', fill_type='solid')
    
    align_center = Alignment(horizontal='center', vertical='center')
    align_left = Alignment(horizontal='left', vertical='center')
    align_right = Alignment(horizontal='right', vertical='center')
    
    thin_side = Side(border_style="thin", color="CBD5E1")
    border_all = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)

    # 1. Título / Banner
    ws.merge_cells('A1:H2')
    title_cell = ws['A1']
    title_cell.value = f"REPORTE MENSUAL DE SERVICIOS - {nombre_mes.upper()} {anio}"
    title_cell.font = font_title
    title_cell.fill = fill_navy
    title_cell.alignment = align_center

    # 2. Información del Técnico / Generación
    ws['A4'] = "Técnico:"
    ws['A4'].font = font_bold
    ws['B4'] = request.user.nombre_completo
    ws['B4'].font = font_body

    ws['A5'] = "Correo:"
    ws['A5'].font = font_bold
    ws['B5'] = request.user.correo
    ws['B5'].font = font_body

    ws['G4'] = "Generación:"
    ws['G4'].font = font_bold
    ws['H4'] = hoy.strftime('%d/%m/%Y')
    ws['H4'].font = font_body

    # 3. KPIs
    ws['A7'] = "KPIs del Periodo"
    ws['A7'].font = font_section

    ws['A8'] = "Métrica"
    ws['A8'].font = font_header
    ws['A8'].fill = fill_navy
    ws['A8'].alignment = align_center
    ws['B8'] = "Valor"
    ws['B8'].font = font_header
    ws['B8'].fill = fill_navy
    ws['B8'].alignment = align_center

    metrics = [
        ("Total Citas", total),
        ("Finalizadas", finalizadas),
        ("Canceladas", canceladas),
        ("Pendientes", pendientes),
        ("Tasa Completado", tasa)
    ]
    for idx, (m_name, m_val) in enumerate(metrics, start=9):
        ws[f'A{idx}'] = m_name
        ws[f'A{idx}'].font = font_bold
        ws[f'A{idx}'].border = border_all
        ws[f'A{idx}'].fill = fill_gray
        
        ws[f'B{idx}'] = m_val
        ws[f'B{idx}'].font = font_body
        ws[f'B{idx}'].border = border_all
        ws[f'B{idx}'].alignment = align_center

    # 4. Tabla de Citas
    ws['A15'] = "Detalle de Citas"
    ws['A15'].font = font_section

    headers = ["#", "Fecha", "Horario", "Cliente", "Servicio", "Estado", "Retraso", "Observaciones"]
    for col_idx, text in enumerate(headers, start=1):
        cell = ws.cell(row=17, column=col_idx, value=text)
        cell.font = font_header
        cell.fill = fill_navy
        cell.alignment = align_center
        cell.border = border_all

    row_num = 18
    if total == 0:
        ws.merge_cells('A18:H18')
        empty_cell = ws['A18']
        empty_cell.value = "Sin citas registradas en este período."
        empty_cell.font = font_body
        empty_cell.alignment = align_center
        for col_idx in range(1, 9):
            ws.cell(row=18, column=col_idx).border = border_all
    else:
        for idx, c in enumerate(citas, start=1):
            ws.cell(row=row_num, column=1, value=f"{idx:02d}").alignment = align_center
            ws.cell(row=row_num, column=2, value=c.fecha.strftime('%d/%m/%Y')).alignment = align_center
            ws.cell(row=row_num, column=3, value=f"{c.hora_inicio.strftime('%H:%M')} – {c.hora_fin.strftime('%H:%M')}").alignment = align_center
            ws.cell(row=row_num, column=4, value=c.cliente.nombre_completo)
            ws.cell(row=row_num, column=5, value=c.servicio.nombre if c.servicio else '—')
            ws.cell(row=row_num, column=6, value=c.estado.nombre if c.estado else '—').alignment = align_center
            ws.cell(row=row_num, column=7, value=f"{c.minutos_retraso} min" if c.minutos_retraso > 0 else '—').alignment = align_center
            ws.cell(row=row_num, column=8, value=c.observaciones if c.observaciones else '—')

            for col_idx in range(1, 9):
                cell = ws.cell(row=row_num, column=col_idx)
                cell.font = font_body
                cell.border = border_all
                if idx % 2 == 0:
                    cell.fill = fill_gray
            row_num += 1

    # Ajustar ancho de columnas (evita MergedCell sin column_letter)
    from openpyxl.utils import get_column_letter
    for col_idx in range(1, 9):
        max_len = 0
        col_letter = get_column_letter(col_idx)
        for row in ws.iter_rows(min_row=3, min_col=col_idx, max_col=col_idx):
            for cell in row:
                try:
                    if cell.value:
                        max_len = max(max_len, len(str(cell.value)))
                except Exception:
                    pass
        ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=Reporte_Servicios_{mes}_{anio}.xlsx'
    wb.save(response)
    return response



@login_required
def cliente_inicio(request):
    """Dashboard principal del cliente (Inicio)"""
    if request.user.rol != Usuario.Rol.CLIENTE:
        return redirect('home')
        
    citas_usuario = Cita.objects.filter(cliente=request.user).order_by('-fecha', '-hora_inicio')
    
    total_citas_activas = citas_usuario.exclude(estado__nombre__in=['Finalizada', 'Cancelada']).count()
    total_reparaciones = citas_usuario.filter(estado__nombre='Finalizada').count()
    
    citas_recientes = citas_usuario
    
    context = {
        'total_citas_activas': total_citas_activas,
        'total_reparaciones': total_reparaciones,
        'citas_recientes': citas_recientes,
    }
    return render(request, 'turnos/cliente/cliente_inicio.html', context)

@login_required
def cliente_servicios(request):
    """Catálogo de servicios para el cliente"""
    if request.user.rol != Usuario.Rol.CLIENTE:
        return redirect('home')
    return render(request, 'turnos/cliente/cliente_servicios.html')

@login_required
def cliente_perfil(request):
    """Perfil del cliente: permite editar datos personales."""
    if request.user.rol != Usuario.Rol.CLIENTE:
        return redirect('home')

    if request.method == 'POST':
        form = EditarPerfilForm(
            request.POST,
            instance=request.user,
            current_user=request.user,
        )
        if form.is_valid():
            form.save()
            messages.success(request, '¡Tus datos personales fueron actualizados correctamente!')
            return redirect('cliente_perfil')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = EditarPerfilForm(instance=request.user, current_user=request.user)

    return render(request, 'turnos/cliente/cliente_perfil.html', {'form': form})

@login_required
def cliente_soporte(request):
    """Página de soporte para el cliente"""
    if request.user.rol != Usuario.Rol.CLIENTE:
        return redirect('home')
    return render(request, 'turnos/cliente/cliente_soporte.html')


@login_required
def tecnico_perfil(request):
    """Perfil del técnico para ver métricas y actualizar información personal."""
    if request.user.rol != Usuario.Rol.TECNICO:
        return redirect('home')

    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=request.user, current_user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Tu perfil técnico fue actualizado con éxito!')
            return redirect('tecnico_perfil')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = EditarPerfilForm(instance=request.user, current_user=request.user)

    return render(request, 'turnos/tecnico/tecnico_perfil.html', {'form': form})


@login_required
def exportar_inventario_excel(request):
    """Exporta la lista de repuestos del técnico a un archivo Excel (.xlsx)."""
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from django.http import HttpResponse

    if request.user.rol != Usuario.Rol.TECNICO:
        return redirect('home')

    repuestos = Repuesto.objects.filter(activo=True).order_by('categoria', 'nombre')

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Inventario Repuestos"
    ws.views.sheetView[0].showGridLines = True

    # Estilos
    font_title = Font(name='Arial', size=14, bold=True, color='FFFFFF')
    font_header = Font(name='Arial', size=10, bold=True, color='FFFFFF')
    font_body = Font(name='Arial', size=10)
    font_bold = Font(name='Arial', size=10, bold=True)
    
    fill_navy = PatternFill(start_color='002B75', end_color='002B75', fill_type='solid')
    fill_gray = PatternFill(start_color='F8FAFC', end_color='F8FAFC', fill_type='solid')
    
    align_center = Alignment(horizontal='center', vertical='center')
    align_left = Alignment(horizontal='left', vertical='center')
    align_right = Alignment(horizontal='right', vertical='center')
    
    thin_side = Side(border_style="thin", color="CBD5E1")
    border_all = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)

    # 1. Título
    ws.merge_cells('A1:E2')
    title_cell = ws['A1']
    title_cell.value = "INVENTARIO DE REPUESTOS Y COMPONENTES"
    title_cell.font = font_title
    title_cell.fill = fill_navy
    title_cell.alignment = align_center

    # Headers
    headers = ["Componente", "Categoría", "Stock (Unidades)", "Precio Unitario", "Estado"]
    for col_idx, text in enumerate(headers, start=1):
        cell = ws.cell(row=4, column=col_idx, value=text)
        cell.font = font_header
        cell.fill = fill_navy
        cell.alignment = align_center
        cell.border = border_all

    row_num = 5
    for idx, r in enumerate(repuestos, start=1):
        ws.cell(row=row_num, column=1, value=r.nombre)
        ws.cell(row=row_num, column=2, value=r.get_categoria_display()).alignment = align_center
        ws.cell(row=row_num, column=3, value=r.stock).alignment = align_center
        
        cell_precio = ws.cell(row=row_num, column=4, value=float(r.precio))
        cell_precio.number_format = '$#,##0.00'
        cell_precio.alignment = align_right
        
        estado = "Disponible" if r.stock > 5 else ("Stock Bajo" if r.stock > 0 else "Agotado")
        ws.cell(row=row_num, column=5, value=estado).alignment = align_center

        for col_idx in range(1, 6):
            cell = ws.cell(row=row_num, column=col_idx)
            cell.font = font_body
            cell.border = border_all
            if idx % 2 == 0:
                cell.fill = fill_gray
        row_num += 1

    # Ajustar columnas (evita MergedCell sin column_letter)
    from openpyxl.utils import get_column_letter
    for col_idx in range(1, 6):
        max_len = 0
        col_letter = get_column_letter(col_idx)
        for row in ws.iter_rows(min_row=3, min_col=col_idx, max_col=col_idx):
            for cell in row:
                try:
                    if cell.value:
                        max_len = max(max_len, len(str(cell.value)))
                except Exception:
                    pass
        ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Inventario_Repuestos.xlsx'
    wb.save(response)
    return response


@login_required
def agregar_repuesto(request):
    """Agrega un nuevo repuesto a la base de datos."""
    if request.user.rol != Usuario.Rol.TECNICO:
        return redirect('home')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        categoria = request.POST.get('categoria')
        stock = request.POST.get('stock', 0)
        precio = request.POST.get('precio', 0.0)

        try:
            Repuesto.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                categoria=categoria,
                stock=int(stock),
                precio=float(precio)
            )
            messages.success(request, f'¡El repuesto "{nombre}" fue agregado con éxito!')
        except Exception as e:
            messages.error(request, f'Error al agregar repuesto: {str(e)}')

    return redirect('tecnico_dispositivos')


# ─────────────────────────────────────────────
#  GESTIÓN DE USUARIOS (ADMIN)
# ─────────────────────────────────────────────
@login_required
def admin_usuarios(request):
    if request.user.rol != Usuario.Rol.ADMINISTRADOR:
        return redirect('home')
    usuarios = Usuario.objects.all().order_by('-fecha_registro')
    return render(request, 'turnos/administracion/admin_usuarios.html', {'usuarios': usuarios})


@login_required
def admin_crear_usuario(request):
    if request.user.rol != Usuario.Rol.ADMINISTRADOR:
        return redirect('home')
    if request.method == 'POST':
        nombre   = request.POST.get('nombre_completo', '').strip()
        correo   = request.POST.get('correo', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        rol      = request.POST.get('rol', Usuario.Rol.CLIENTE)
        password = request.POST.get('password', '')
        if not nombre or not correo or not password:
            messages.error(request, 'Nombre, correo y contraseña son obligatorios.')
        elif Usuario.objects.filter(correo=correo).exists():
            messages.error(request, f'Ya existe un usuario con el correo {correo}.')
        else:
            try:
                Usuario.objects.create_user(correo=correo, password=password,
                    nombre_completo=nombre, telefono=telefono or None, rol=rol)
                messages.success(request, f'Usuario "{nombre}" creado correctamente.')
            except Exception as e:
                messages.error(request, f'Error: {e}')
    return redirect('admin_usuarios')


@login_required
def admin_editar_usuario(request, usuario_id):
    if request.user.rol != Usuario.Rol.ADMINISTRADOR:
        return redirect('home')
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    if request.method == 'POST':
        usuario.nombre_completo = request.POST.get('nombre_completo', usuario.nombre_completo).strip()
        usuario.correo          = request.POST.get('correo', usuario.correo).strip()
        usuario.telefono        = request.POST.get('telefono', '').strip() or None
        usuario.rol             = request.POST.get('rol', usuario.rol)
        try:
            usuario.save()
            messages.success(request, f'Usuario "{usuario.nombre_completo}" actualizado.')
        except Exception as e:
            messages.error(request, f'Error: {e}')
    return redirect('admin_usuarios')


@login_required
def admin_toggle_usuario(request, usuario_id):
    if request.user.rol != Usuario.Rol.ADMINISTRADOR:
        return redirect('home')
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    if request.method == 'POST':
        if usuario.pk == request.user.pk:
            messages.error(request, 'No puedes desactivar tu propia cuenta.')
        else:
            usuario.activo = not usuario.activo
            usuario.save()
            messages.success(request, f'Usuario "{usuario.nombre_completo}" {"activado" if usuario.activo else "desactivado"}.')
    return redirect('admin_usuarios')


# ─────────────────────────────────────────────
#  CATÁLOGO DE SERVICIOS (ADMIN)
# ─────────────────────────────────────────────
@login_required
def admin_servicios(request):
    if request.user.rol != Usuario.Rol.ADMINISTRADOR:
        return redirect('home')
    servicios      = Servicio.objects.select_related('especialidad').order_by('tipo_dispositivo', 'nombre')
    especialidades = Especialidad.objects.filter(activo=True).order_by('nombre')
    return render(request, 'turnos/administracion/admin_servicios.html',
                  {'servicios': servicios, 'especialidades': especialidades})


@login_required
def admin_crear_servicio(request):
    if request.user.rol != Usuario.Rol.ADMINISTRADOR:
        return redirect('home')
    if request.method == 'POST':
        nombre   = request.POST.get('nombre', '').strip()
        desc     = request.POST.get('descripcion', '').strip()
        tipo     = request.POST.get('tipo_dispositivo', 'CELULAR')
        duracion = int(request.POST.get('duracion_minutos', 60))
        buffer   = int(request.POST.get('buffer_minutos', 0))
        esp_id   = request.POST.get('especialidad_id')
        if not nombre:
            messages.error(request, 'El nombre es obligatorio.')
        else:
            try:
                especialidad = get_object_or_404(Especialidad, pk=esp_id)
                Servicio.objects.create(nombre=nombre, descripcion=desc or None,
                    tipo_dispositivo=tipo, duracion_minutos=duracion,
                    buffer_minutos=buffer, especialidad=especialidad)
                messages.success(request, f'Servicio "{nombre}" creado.')
            except Exception as e:
                messages.error(request, f'Error: {e}')
    return redirect('admin_servicios')


@login_required
def admin_editar_servicio(request, servicio_id):
    if request.user.rol != Usuario.Rol.ADMINISTRADOR:
        return redirect('home')
    servicio = get_object_or_404(Servicio, pk=servicio_id)
    if request.method == 'POST':
        servicio.nombre           = request.POST.get('nombre', servicio.nombre).strip()
        servicio.descripcion      = request.POST.get('descripcion', '').strip() or None
        servicio.tipo_dispositivo = request.POST.get('tipo_dispositivo', servicio.tipo_dispositivo)
        servicio.duracion_minutos = int(request.POST.get('duracion_minutos', servicio.duracion_minutos))
        servicio.buffer_minutos   = int(request.POST.get('buffer_minutos', servicio.buffer_minutos))
        esp_id = request.POST.get('especialidad_id')
        if esp_id:
            servicio.especialidad = get_object_or_404(Especialidad, pk=esp_id)
        try:
            servicio.save()
            messages.success(request, f'Servicio "{servicio.nombre}" actualizado.')
        except Exception as e:
            messages.error(request, f'Error: {e}')
    return redirect('admin_servicios')


@login_required
def admin_toggle_servicio(request, servicio_id):
    if request.user.rol != Usuario.Rol.ADMINISTRADOR:
        return redirect('home')
    servicio = get_object_or_404(Servicio, pk=servicio_id)
    if request.method == 'POST':
        servicio.activo = not servicio.activo
        servicio.save()
        messages.success(request, f'Servicio "{servicio.nombre}" {"activado" if servicio.activo else "desactivado"}.')
    return redirect('admin_servicios')


# ─────────────────────────────────────────────
#  CITAS (ADMIN)
# ─────────────────────────────────────────────
@login_required
def admin_citas(request):
    if request.user.rol != Usuario.Rol.ADMINISTRADOR:
        return redirect('home')
    citas = Cita.objects.select_related('cliente', 'tecnico', 'servicio', 'estado').order_by('-fecha', '-hora_inicio')
    return render(request, 'turnos/administracion/admin_citas.html',
                  {'citas': citas, 'total_citas': citas.count()})


# ─────────────────────────────────────────────
#  REPORTES (ADMIN)
# ─────────────────────────────────────────────
@login_required
def admin_reportes(request):
    if request.user.rol != Usuario.Rol.ADMINISTRADOR:
        return redirect('home')
    hoy = date.today()
    citas_mes_qs = Cita.objects.filter(fecha__year=hoy.year, fecha__month=hoy.month)
    total       = citas_mes_qs.count()
    finalizadas = citas_mes_qs.filter(estado__nombre__iexact='Finalizada').count()
    canceladas  = citas_mes_qs.filter(estado__nombre__iexact='Cancelada').count()
    tasa_exito  = round(finalizadas / total * 100, 1) if total > 0 else 0

    servicios_populares = (Cita.objects
        .filter(fecha__year=hoy.year, fecha__month=hoy.month)
        .values('servicio__nombre').annotate(total=Count('id')).order_by('-total')[:5])

    tecnicos_top = (Cita.objects
        .filter(fecha__year=hoy.year, fecha__month=hoy.month, tecnico__isnull=False)
        .values('tecnico__nombre_completo').annotate(total=Count('id')).order_by('-total')[:5])

    MESES_ES = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
    citas_por_mes = []
    max_val = 1
    for i in range(5, -1, -1):
        primer_dia = date(hoy.year, hoy.month, 1)
        mes_obj = primer_dia
        for _ in range(i):
            mes_obj = (mes_obj.replace(day=1) - timedelta(days=1)).replace(day=1)
        ultimo = calendar.monthrange(mes_obj.year, mes_obj.month)[1]
        cnt = Cita.objects.filter(fecha__gte=mes_obj, fecha__lte=mes_obj.replace(day=ultimo)).count()
        citas_por_mes.append({'mes_label': MESES_ES[mes_obj.month - 1], 'total': cnt})
        if cnt > max_val:
            max_val = cnt

    context = {
        'reporte': {'total': total, 'finalizadas': finalizadas, 'canceladas': canceladas, 'tasa_exito': tasa_exito},
        'servicios_populares': servicios_populares,
        'tecnicos_top':        tecnicos_top,
        'citas_por_mes':       citas_por_mes,
        'citas_por_mes_max':   max_val,
    }
    return render(request, 'turnos/administracion/admin_reportes.html', context)
