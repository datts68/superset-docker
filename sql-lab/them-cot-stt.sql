-- Thêm cột STT ở đầu bảng
SELECT 
    ROW_NUMBER() OVER(ORDER BY tong_giao_dich DESC) AS "STT",
    t.status_code,
    t.tong_giao_dich,
    t.ty_le_phan_tram
FROM (
    SELECT 
        status_code,
        COUNT(*) AS tong_giao_dich,
        ROUND(
            (100.0 * COUNT(*)) / SUM(COUNT(*)) OVER (), 
            2
        ) AS ty_le_phan_tram
    FROM ndop.analytic_offloads
    GROUP BY status_code
) t
ORDER BY t.tong_giao_dich DESC
