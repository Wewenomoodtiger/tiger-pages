#!/usr/bin/env python3
"""Extract running workouts from Apple Health export.xml"""
import xml.etree.ElementTree as ET
import sys

filepath = r"C:\Users\Tiger Ng\Desktop\新建文件夹\export\apple_health_export\export.xml"
print("正在提取跑步数据，请稍候...")

workouts = []
count = 0
for event, elem in ET.iterparse(filepath, events=("end",)):
    if elem.tag == "Workout":
        atype = elem.attrib.get("workoutActivityType", "")
        if "Running" in atype or "Run" in atype:
            dist_elem = elem.find("WorkoutStatistics[@type='HKQuantityTypeIdentifierDistanceWalkingRunning']")
            energy_elem = elem.find("WorkoutStatistics[@type='HKQuantityTypeIdentifierActiveEnergyBurned']")
            hr_elem = elem.find("WorkoutStatistics[@type='HKQuantityTypeIdentifierHeartRate']")
            
            # Apple Health XML export uses minutes for duration
            duration_val = float(elem.attrib.get("duration", 0))
            distance_km = round(float(dist_elem.attrib.get("sum", 0)) if dist_elem is not None else 0, 2)
            calories = round(float(energy_elem.attrib.get("sum", 0)) if energy_elem is not None else 0, 0)
            avg_hr = round(float(hr_elem.attrib.get("average", 0))) if hr_elem is not None else 0
            pace = round(duration_val / distance_km, 2) if distance_km > 0 else 0
            
            workouts.append({
                "date": elem.attrib.get("startDate", "")[:10],
                "distance_km": distance_km,
                "duration_min": round(duration_val, 1),
                "pace_per_km": pace,
                "calories": calories,
                "avg_hr": avg_hr,
            })
            count += 1
        elem.clear()
    
    if count > 0 and count % 50 == 0:
        sys.stdout.write(f"   已处理 {count} 条...\r")
        sys.stdout.flush()

sys.stdout.write("\n\n")
workouts.sort(key=lambda x: x["date"], reverse=True)
print(f"共找到 {len(workouts)} 条跑步记录！\n")

# Only show runs with significant distance (>= 1km)
sig_runs = [w for w in workouts if w["distance_km"] >= 1.0]
print(f"有效跑步（>=1km）: {len(sig_runs)} 次\n")

print("最近20次跑步：")
print(f"{'日期':<12} {'距离(km)':<10} {'用时(min)':<10} {'配速(/km)':<12} {'心率':<6} {'卡路里':<8}")
print("-" * 58)
for w in sig_runs[:20]:
    p = f"{w['pace_per_km']:.1f}" if w["pace_per_km"] > 0 else "N/A"
    hr = str(w["avg_hr"]) if w["avg_hr"] > 0 else "-"
    print(f"{str(w['date']):<12} {str(w['distance_km']):<10} {str(w['duration_min']):<10} {p:<12} {hr:<6} {str(w['calories']):<8}")

if sig_runs:
    total_dist = sum(w["distance_km"] for w in sig_runs)
    total_runs = len(sig_runs)
    fast_runs = [w for w in sig_runs if w["pace_per_km"] > 0]
    fastest = min(fast_runs, key=lambda x: x["pace_per_km"]) if fast_runs else None
    avg_pace_all = sum(w["pace_per_km"] for w in fast_runs) / len(fast_runs) if fast_runs else 0
    
    import datetime
    dates = [w["date"] for w in sig_runs]
    latest = max(dates) if dates else ""
    earliest = min(dates) if dates else ""
    total_duration = sum(w["duration_min"] for w in sig_runs)
    
    # Monthly breakdown
    monthly = {}
    for w in sig_runs:
        m = w["date"][:7]
        if m not in monthly:
            monthly[m] = {"runs": 0, "dist": 0, "time": 0}
        monthly[m]["runs"] += 1
        monthly[m]["dist"] += w["distance_km"]
        monthly[m]["time"] += w["duration_min"]
    
    print("\n--- 数据总结 ---")
    print(f"   总跑步次数: {total_runs}")
    print(f"   总距离:     {total_dist:.1f} km")
    print(f"   总用时:     {total_duration:.0f} 分 ({total_duration/60:.0f} 小时)")
    print(f"   平均每次:   {total_dist/total_runs:.2f} km")
    print(f"   平均配速:   {avg_pace_all:.1f} min/km")
    if fastest:
        print(f"   最快配速:   {fastest['pace_per_km']:.1f} min/km ({fastest['date']})")
    hrs_with_hr = [w for w in sig_runs if w["avg_hr"] > 0]
    if hrs_with_hr:
        avg_hr_all = sum(w["avg_hr"] for w in hrs_with_hr) / len(hrs_with_hr)
        print(f"   平均心率:   {avg_hr_all:.0f} bpm")
    print(f"   时间跨度:   {earliest} ~ {latest}")
    
    print("\n--- 月跑量走势 ---")
    for m in sorted(monthly.keys()):
        d = monthly[m]
        bar = "#" * min(round(d["dist"] / 5), 60)
        print(f"   {m}: {d['runs']:2d}次 {d['dist']:5.1f}km ({d['time']/60:.1f}h) {bar}")
