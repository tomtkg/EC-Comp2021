function make_image()
    load data.mat data %data = [naha42, naha256, hako42, hako256];
    for i = 1 : 8
        figure('Position',[100 100 480,360],'Visible','on');
        set(gca,'Fontname','Times New Roman','FontSize',13,'NextPlot','add', ...
            'Color','none','Box','on','LooseInset', get(gca, 'TightInset'));
        C = {'k-o','k:+','b-o','b:+','r-o','r:+'};
        if i < 5
            s = 18*(i-1); yint = 1; ystr =  '目的関数値f';
        else
            s = 18*(i-5); yint = 0; ystr =  '支給金額pay';
        end
        for j = 1 : 6
            k = find(data(:,s+3*j-2));
            p(j) = plot(data(k,s+3*j-2), data(k,s+3*j-yint),C{j},'MarkerSize',3);
        end
        xlabel('関数評価回数','FontName','ＭＳ 明朝');
        ylabel(ystr,'FontName','ＭＳ 明朝');
        label = ["従来の最適化 従来の定式化","従来の最適化 提案の定式化",...
            " fのみ考慮   b=0スタート"," fのみ考慮   b=1スタート",...
            " f,pay考慮   b=0スタート"," f,pay考慮   b=1スタート"];
        legend(p,label,'Color','white','FontName','ＭＳ 明朝');
        %axis square;
        exportgraphics(gcf,[num2str(i),'.eps'],'BackgroundColor','none','ContentType','vector');
        savefig([num2str(i),'.fig']);
        close;
    end
end
