
-- set @communtiy = '合景叠翠峰';
-- set @communtiy = '尹山湖韵佳苑';
-- set @communtiy =  '保利悦玺';
set @communtiy =  '保利居上';

-- 当前房源详细
SELECT * FROM ershoufang.houseinfo 
where community = @communtiy order by decoration desc,(unitPrice+0);

-- 查询80平到100平的房源
SELECT 
    housetype,
    LEFT(floor, 1) AS floor,
    ROUND(totalPrice * 10000 / unitPrice) AS square,
    decoration,
    case 
		when locate("车位", title) > 0 then 1 
		else 0
	end as '车位',
    totalPrice, unitPrice, link
FROM
    ershoufang.houseinfo
WHERE
    community = @communtiy
        AND totalPrice * 10000 / unitPrice BETWEEN 80 AND 100
ORDER BY square , decoration DESC , (unitPrice + 0);

-- 当前房源价格信息
SELECT * FROM ershoufang.hisprice where community = @communtiy;

-- 已售房源信息
SELECT * FROM ershoufang.sellinfo where community = @communtiy order by dealdate desc;

delete from ershoufang.houseinfo where community = @communtity;
delete from ershoufang.hisprice where community = @communtity;
delete from ershoufang.sellinfo where community = @communtity;
